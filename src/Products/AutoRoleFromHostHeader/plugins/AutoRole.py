# -*- coding: utf-8 -*-

from AccessControl.SecurityInfo import ClassSecurityInfo
from Globals import InitializeClass
from Products.AutoRoleFromHostHeader.interfaces import ConfigurationChangedEvent
from Products.PageTemplates.Expressions import createZopeEngine
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin
from Products.PluggableAuthService.interfaces.plugins import IExtractionPlugin
from Products.PluggableAuthService.interfaces.plugins import IGroupsPlugin
from Products.PluggableAuthService.interfaces.plugins import IRolesPlugin
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements
from zope.event import notify
import re

manage_addAutoRoleForm = PageTemplateFile(
    'www/autoRoleAdd', globals(), __name__='manage_addAutoRoleForm')


def addAutoRole( dispatcher
               , id
               , title=None
               , match_roles=()
               , REQUEST=None
               ):
    """ Add an AutoRole plugin to a Pluggable Auth Service. """
    sp = AutoRole(id, title, match_roles)
    dispatcher._setObject(sp.getId(), sp)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect( '%s/manage_workspace'
                                      '?manage_tabs_message='
                                      'AutoRole+added.'
                                    % dispatcher.absolute_url() )

class AutoRole(BasePlugin):
    """ Multi-plugin for assigning auto roles from IP. """

    meta_type = 'Auto Role Header Plugin'
    security = ClassSecurityInfo()

    _properties = (
        dict(id='title', label='Title', type='string', mode='w'),
        dict(id='match_roles', label='Header name; regexp; roles/groups ; TALES condition expression', type='lines',
             mode='w'),
        dict(id='anon_only', label='Anonymous Only', type='boolean',
             mode='w'),
    )
    
    anon_only = False

    def __init__(self, id, title=None, match_roles=()):
        self._setId(id)
        self.title = title
        self.match_roles = match_roles
        self.anon_only = False
        self._compiled = []
    
    def _compile_matchs(self):
        self._compiled = compiled = []
        for line in self.match_roles:
            try:
                values = line.split(';')
                if len(values) == 3:
                    # If there isn't a condition, pretend the condition was
                    # something that's always true
                    values = values + ['python:True',]
                header_name, regexp, roles, condition = values
                roles = [r.strip() for r in roles.split(',')]
                roles = set(filter(None, roles))
                if not roles:
                    continue
            except (ValueError, AttributeError):
                continue
            compiled.append((header_name, regexp, roles, condition))
            
    def _setPropValue(self, id, value):
        BasePlugin._setPropValue(self, id, value)
        if id == 'match_roles':
            self._compile_matchs()
            if value and len(self._compiled) != len(self.match_roles):
                raise ValueError(
                    'match_roles contains invalid parameters!')
            notify(ConfigurationChangedEvent(self))

    #
    # IRolesPlugin
    #
    security.declarePrivate('getRolesForPrincipal')
    def getRolesForPrincipal(self, principal, request=None):
        """ Assign roles based on 'request'. """
        # we need this for uncontexted calls
        if request is None:
            return []
        engine = createZopeEngine()
        if (self.anon_only and 
                principal is not None and 
                principal.getUserName() != 'Anonymous User'):
            return []
        if not self._compiled:
            return []

        result = set()
        context = engine.getContext(request=request, portal=self._getPAS().aq_parent.aq_inner)
        print self._getPAS().aq_parent.aq_inner
        for header_name, regexp, roles, condition in self._compiled:
            condition = engine.compile(condition)
            header = request.get(header_name)
            if header:
                check_header = re.compile(regexp)
                if check_header.match(header) and condition(context):
                    result.update(roles)
        return list(result)

    #
    # IGroupsPlugin
    #
    # This method allows the plugin to be used to assign groups instead of
    # roles if used as a group plugin instead of a role plugin.
    security.declarePrivate('getGroupsForPrincipal')
    def getGroupsForPrincipal(self, principal, request=None):
        """ Assign groups based on 'request'. """
        return self.getRolesForPrincipal(principal, request)

    #
    # IExtractionPlugin
    #
    security.declarePrivate('extractCredentials')
    def extractCredentials(self, request):
        # Avoid creating anon user if this is a regular user
        # We actually have to poke request ourselves to avoid users from
        # root becoming anonymous...
        engine = createZopeEngine()
        if getattr(request, '_auth', None):
            return {}
        
        if not self._compiled:
            return {}
        
        context = engine.getContext(request=request, portal=self._getPAS().aq_parent.aq_inner)
        site = self._getPAS().aq_parent.aq_inner
        for header_name, regexp, roles, condition in self._compiled:
            condition = engine.compile(condition)
            header = request.get(header_name)
            if header:
                check_header = re.compile(regexp)
                if check_header.match(header) and condition(context):
                    return dict(AutoRole=True)

        return {}

    #
    # IAuthenticationPlugin
    #
    security.declarePrivate('authenticateCredentials')
    def authenticateCredentials(self, credentials):
        # Make sure we don't instantiate anonymous if there are other credentials
        # BBB: this seems only work for basic authentication. Can we do something better?
        if credentials.get('login'):
            return None
        autorole = credentials.get('AutoRole', None)
        if not autorole:
            return None
        return ('Anonymous User', 'Anonymous User')


classImplements( AutoRole
               , IRolesPlugin
               , IGroupsPlugin
               , IExtractionPlugin
               , IAuthenticationPlugin
               )

InitializeClass(AutoRole)
