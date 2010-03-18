import unittest

from zope.component import eventtesting
from zope.testing import cleanup


class TestEvent(unittest.TestCase):

    def setUp(self):
        eventtesting.setUp()

    def tearDown(self):
        cleanup.cleanUp()

    def _getTargetClass(self):
        from Products.AutoRoleFromHostHeader.plugins.AutoRole import AutoRole
        return AutoRole

    def _makeOne(self, id='test', *args, **kw):
        return self._getTargetClass()(id=id, *args, **kw)

    def testChangingHEaderMatchFiresEvent(self):
        plugin = self._makeOne()
        self.assertEqual(eventtesting.getEvents(), [])
        plugin.manage_changeProperties(match_roles=[r'REMOTE_ADDR;^10\.0\.(100|101)\.;Authenticated,Member'])
        self.assertEqual(len(eventtesting.getEvents()), 1)
        event = eventtesting.getEvents()[0]
        self.assertEqual(event.__class__.__name__, 'ConfigurationChangedEvent')
        self.assertEqual(event.object, plugin)
        self.assertEqual(event.object.match_roles, (r'REMOTE_ADDR;^10\.0\.(100|101)\.;Authenticated,Member',))

    def testChangingTitleFiresNoEvent(self):
        plugin = self._makeOne()
        self.assertEqual(eventtesting.getEvents(), [])
        plugin.manage_changeProperties(title='Foo')
        self.assertEqual(eventtesting.getEvents(), [])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestEvent))
    return suite

