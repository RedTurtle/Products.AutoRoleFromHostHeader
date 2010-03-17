from zope.interface import implements

from zope.component.interfaces import IObjectEvent
from zope.component.interfaces import ObjectEvent


class IConfigurationChangedEvent(IObjectEvent):
    """Fired when the ip_roles property has changed."""

class ConfigurationChangedEvent(ObjectEvent):
    implements(IConfigurationChangedEvent)
