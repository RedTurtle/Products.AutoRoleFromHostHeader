from AccessControl.Permissions import add_user_folders
from Products.PluggableAuthService import registerMultiPlugin
from Products.AutoRoleFromHostHeader.plugins import AutoRole

registerMultiPlugin(AutoRole.AutoRole.meta_type)

def initialize(context):
    context.registerClass(AutoRole.AutoRole,
                          permission=add_user_folders,
                          constructors=(AutoRole.manage_addAutoRoleForm,
                                        AutoRole.addAutoRole),
                          visibility=None)
