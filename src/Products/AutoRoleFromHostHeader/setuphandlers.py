
def setup_auto_role_plugin(portal):
    uf = portal.acl_users
    ids = uf.objectIds()

    if 'auto_role_header' not in ids:
        factory = uf.manage_addProduct['AutoRoleFromHostHeader']
        factory.addAutoRole('auto_role_header', 'Automatic Role Provider from HTTP Header')

        plugin = uf['auto_role_header']
        plugin.manage_activateInterfaces(['IExtractionPlugin',
                                          'IAuthenticationPlugin',
                                          'IRolesPlugin'])


def importVarious(context):
    site = context.getSite()
    logger = context.getLogger('autorole_header')

    if context.readDataFile('autorole.txt') is None:
        logger.info('Nothing to import.')
        return

    setup_auto_role_plugin(site)
    logger.info('PAS plugin imported.')
