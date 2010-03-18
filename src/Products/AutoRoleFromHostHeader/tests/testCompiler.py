import unittest

def compiled(plugin):
    plugin._compile_subnets()
    return plugin._compiled


class TestCompiler(unittest.TestCase):

    def _getTargetClass(self):
        from Products.AutoRoleFromHostHeader.plugins.AutoRole import AutoRole
        return AutoRole

    def _makeOne(self, id='test', *args, **kw):
        return self._getTargetClass()(id=id, *args, **kw)

    def testTwoRoles(self):
        plugin = self._makeOne(match_roles=[r'REMOTE_ADDR;127\.0\.0\.;Manager,Member'])
        self.assertEqual(compiled(plugin), [('REMOTE_ADDR', '127\\.0\\.0\\.', set(['Member', 'Manager']))])

    def testDuplicateRole(self):
        plugin = self._makeOne(match_roles=[r'REMOTE_ADDR;127\.0\.0\.;Manager,Manager'])
        self.assertEqual(compiled(plugin), [('REMOTE_ADDR', '127\\.0\\.0\\.', set(['Manager']))])

    def testWhitespace(self):
        plugin = self._makeOne(match_roles=[r'REMOTE_ADDR;127\.0\.0\.; Manager, Member'])
        self.assertEqual(compiled(plugin), [('REMOTE_ADDR', '127\\.0\\.0\\.', set(['Manager', 'Member']))])

    def testNoIp(self):
        plugin = self._makeOne(match_roles=[':Manager'])
        self.assertEqual(compiled(plugin), [])

    def testNoRole(self):
        plugin = self._makeOne(match_roles=['xxxx;'])
        self.assertEqual(compiled(plugin), [])

    def testNoColon(self):
        plugin = self._makeOne(match_roles=['xxxx'])
        self.assertEqual(compiled(plugin), [])

    def testEmptyString(self):
        plugin = self._makeOne(match_roles=[''])
        self.assertEqual(compiled(plugin), [])

    def testEmpty(self):
        plugin = self._makeOne(match_roles=[])
        self.assertEqual(compiled(plugin), [])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCompiler))
    return suite

