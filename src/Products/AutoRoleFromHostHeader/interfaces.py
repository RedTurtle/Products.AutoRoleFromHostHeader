from zope.component.interfaces import IObjectEvent, ObjectEvent
from zope.interface import implementer


class IConfigurationChangedEvent(IObjectEvent):
    """Fired when the ip_roles property has changed."""

@implementer(IConfigurationChangedEvent)
class ConfigurationChangedEvent(ObjectEvent):
    pass
