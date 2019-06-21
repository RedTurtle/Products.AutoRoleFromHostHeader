from zope.component.interfaces import IObjectEvent, ObjectEvent
from zope.interface import implements


class IConfigurationChangedEvent(IObjectEvent):
    """Fired when the ip_roles property has changed."""

class ConfigurationChangedEvent(ObjectEvent):
    implements(IConfigurationChangedEvent)
