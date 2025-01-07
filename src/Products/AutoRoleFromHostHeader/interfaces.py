from zope.interface import implementer

try:
    from zope.interface.interfaces import IObjectEvent
    from zope.interface.interfaces import ObjectEvent
except ImportError:
    # BBB
    from zope.component.interfaces import IObjectEvent
    from zope.component.interfaces import ObjectEvent


class IConfigurationChangedEvent(IObjectEvent):
    """Fired when the ip_roles property has changed."""

@implementer(IConfigurationChangedEvent)
class ConfigurationChangedEvent(ObjectEvent):
    pass
