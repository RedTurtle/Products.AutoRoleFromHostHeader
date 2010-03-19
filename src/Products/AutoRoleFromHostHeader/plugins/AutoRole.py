import socket
import struct

from zope.event import notify
from Products.AutoRoleFromHostHeader.interfaces import ConfigurationChangedEvent

from AccessControl.SecurityInfo import ClassSecurityInfo
from Globals import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.interfaces.plugins import IRolesPlugin
from Products.PluggableAuthService.interfaces.plugins import IGroupsPlugin
from Products.PluggableAuthService.interfaces.plugins import IExtractionPlugin
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin

try:
    set
except NameError:
    # Python 2.3
    from sets import Set as set

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
        dict(id='match_roles', label='Header name, regexp and roles', type='lines',
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
                header_name, regexp, roles = line.split(';')
                roles = [r.strip() for r in roles.split(',')]
                roles = set(filter(None, roles))
                if not roles:
                    continue
            except (ValueError, AttributeError):
                continue
            compiled.append((header_name, regexp, roles))
            
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
        if (self.anon_only and 
            principal is not None and 
            principal.getUserName() != 'Anonymous User'):
            return []
        if not self._compiled:
            return []

        result = set()
        for header_name, regexp, roles in self._compiled:
            header = request[header_name]
            check_header = re.compile(regexp)
            if check_header.match(header):
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

        if getattr(request, '_auth', None):
            return {}
        
        if not self._compiled:
            return {}

        for header_name, regexp, roles in self._compiled:
            header = request[header_name]
            check_header = re.compile(regexp)
            if check_header.match(header):
                return dict(AutoRole=True)

        return {}

    #
    # IAuthenticationPlugin
    #
    security.declarePrivate('authenticateCredentials')
    def authenticateCredentials(self, credentials):
        if credentials.has_key('login'):
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
