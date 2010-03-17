import unittest

def compiled(plugin):
    plugin._compile_subnets()
    return plugin._compiled


class TestCompiler(unittest.TestCase):

    def _getTargetClass(self):
        from Products.AutoRole.plugins.AutoRole import AutoRole
        return AutoRole

    def _makeOne(self, id='test', *args, **kw):
        return self._getTargetClass()(id=id, *args, **kw)

    def testFullSpec(self):
        plugin = self._makeOne(ip_roles=['127.0.0.1/32:Manager'])
        self.assertEqual(compiled(plugin), [(2130706433L, 4294967295L, set(['Manager']))])

    def testDefaultMaskIs32(self):
        plugin = self._makeOne(ip_roles=['127.0.0.1:Manager'])
        self.assertEqual(compiled(plugin), [(2130706433L, 4294967295L, set(['Manager']))])

    def testTwoRoles(self):
        plugin = self._makeOne(ip_roles=['127.0.0.1/32:Manager,Member'])
        self.assertEqual(compiled(plugin), [(2130706433L, 4294967295L, set(['Manager', 'Member']))])

    def testDuplicateRole(self):
        plugin = self._makeOne(ip_roles=['127.0.0.1/32:Manager,Manager'])
        self.assertEqual(compiled(plugin), [(2130706433L, 4294967295L, set(['Manager']))])

    def testWhitespace(self):
        plugin = self._makeOne(ip_roles=['127.0.0.1/32 : Manager, Member'])
        self.assertEqual(compiled(plugin), [(2130706433L, 4294967295L, set(['Manager', 'Member']))])

    def testNoIp(self):
        plugin = self._makeOne(ip_roles=[':Manager'])
        self.assertEqual(compiled(plugin), [])

    def testNoRole(self):
        plugin = self._makeOne(ip_roles=['127.0.0.1:'])
        self.assertEqual(compiled(plugin), [])

    def testNoColon(self):
        plugin = self._makeOne(ip_roles=['127.0.0.1'])
        self.assertEqual(compiled(plugin), [])

    def testEmptyString(self):
        plugin = self._makeOne(ip_roles=[''])
        self.assertEqual(compiled(plugin), [])

    def testEmpty(self):
        plugin = self._makeOne(ip_roles=[])
        self.assertEqual(compiled(plugin), [])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCompiler))
    return suite

