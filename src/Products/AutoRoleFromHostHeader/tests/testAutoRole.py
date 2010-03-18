#
# AutoRoleTestCase AutoRole
#

import unittest
import UserDict

from Products.PluggableAuthService.tests.conformance \
     import IRolesPlugin_conformance

from AccessControl.User import SimpleUser

ORIGINAL_REMOTE_ADDR = '127.0.0.1'
ORIGINAL_HTTP_USER_AGENT = ('Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; it-it) '
                            'AppleWebKit/531.21.8 (KHTML, like Gecko) '
                            'Version/4.0.4 Safari/531.21.10')

class FakeRequest(UserDict.UserDict):
    client_ip = ''
    _auth = None
    
    REMOTE_ADDR = ORIGINAL_REMOTE_ADDR
    HTTP_USER_AGENT = ORIGINAL_HTTP_USER_AGENT
    
    def __getitem__(self, arg):
        if arg=='REMOTE_ADDR':
            return self.REMOTE_ADDR
        if arg=='HTTP_USER_AGENT':
            return self.HTTP_USER_AGENT

class TestAutoRole(unittest.TestCase, IRolesPlugin_conformance):

    def _getTargetClass(self):
        from Products.AutoRoleFromHostHeader.plugins.AutoRole \
            import AutoRole

        return AutoRole

    def _makeOne( self, id='test', *args, **kw ):
        return self._getTargetClass()( id=id, *args, **kw )

    def test_getRolesForPrincipal( self ):
        helper = self._makeOne()
        request = FakeRequest()

        helper._updateProperty('match_roles', [r'REMOTE_ADDR;127\.0\.0\.;Manager,Member'])
        self.assertEqual( helper.getRolesForPrincipal( None, request ), ['Member','Manager'])

        helper._updateProperty('match_roles', [r'REMOTE_ADDR;127\.0\.0\.;Manager',
                                               r'REMOTE_ADDR;1\.28\.;Member',
                                               r'HTTP_USER_AGENT;Mozilla\/5\.0;Member,Manager'])
        request.REMOTE_ADDR='1.28.1.1'
        request.HTTP_USER_AGENT='Funny 1.0'
        self.assertEqual( helper.getRolesForPrincipal( None, request ), ['Member'])
        request.REMOTE_ADDR='10.0.1.49'
        request.HTTP_USER_AGENT=ORIGINAL_HTTP_USER_AGENT
        self.assertEqual( helper.getRolesForPrincipal( None, request ), ['Member','Manager'])
        
        # Check that only anonymous get roles if anon_only is checked.
        helper.anon_only = True
        request.REMOTE_ADDR = '10.0.1.1'        
        user = SimpleUser('someone', 'something', [], [])
        self.assertEqual( helper.getRolesForPrincipal( user, request ), [])

        user = SimpleUser('Anonymous User', 'something', [], [])
        self.assertEqual( helper.getRolesForPrincipal( user, request ), ['Member','Manager'])
        helper.anon_only = False

        # Test for invalid ip address
        helper._updateProperty('match_roles', [r'REMOTE_ADDR;10\.0\.0\.;Manager',
                                               r'REMOTE_ADDR;10\.1\.0\.;Manager'])
        request.REMOTE_ADDR = 'invalidip'
        self.assertEqual( helper.getRolesForPrincipal( None, request ), [])
        request.REMOTE_ADDR = ''
        self.assertEqual( helper.getRolesForPrincipal( None, request ), [])

    def test_extractCredentials( self ):
        helper = self._makeOne()
        request = FakeRequest()

        helper._updateProperty('match_roles', [r'REMOTE_ADDR;^10\.0\.(100|101)\.;Authenticated,Member'])
        request.REMOTE_ADDR = '10.0.100.1'
        self.assertEqual(helper.extractCredentials( request ), {'AutoRole':True})

        request.REMOTE_ADDR = '10.1.0.0'
        self.assertEqual( helper.extractCredentials( request ), {})

        request._auth = 'Basic' # No extraction if already http auth
        request.client_ip = '10.0.1.1'
        self.assertEqual( helper.extractCredentials( request ), {})

    def test_extractInvalidCredentials( self ):
        helper = self._makeOne()
        request = FakeRequest()

        helper._updateProperty('match_roles', [r'REMOTE_ADDR;^10\.0\.(100|101)\.;Authenticated,Member'])

        request.REMOTE_ADDR = 'invalidip'
        self.assertEqual( helper.extractCredentials( request ), {})

        request.REMOTE_ADDR = ''
        self.assertEqual( helper.extractCredentials( request ), {})

    def test_authenticateCredentials( self ):
        helper = self._makeOne()

        self.assertEqual( helper.authenticateCredentials( {} ), None)
        self.assertEqual( helper.authenticateCredentials( {'AutoRole':True} ), ('Anonymous User','Anonymous User'))
        # Make sure we don't instantiate anonymous if there are other credentials
        self.assertEqual( helper.authenticateCredentials( {'AutoRole':True, 'login':'user','password':'password'} ), None)
        

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestAutoRole))
    return suite
