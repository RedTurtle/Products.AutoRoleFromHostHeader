from AccessControl.Permissions import add_user_folders
from Products.AutoRoleFromHostHeader.plugins import AutoRole
from Products.PluggableAuthService import registerMultiPlugin

registerMultiPlugin(AutoRole.AutoRole.meta_type)

def initialize(context):
    context.registerClass(AutoRole.AutoRole,
                          permission=add_user_folders,
                          constructors=(AutoRole.manage_addAutoRoleForm,
                                        AutoRole.addAutoRole),
                          visibility=None,
                          icon='plugins/www/login_sm.gif'
                          )
