AutoRoleFromHostHeader PAS Plugin
=================================

Add roles to (anonymous or logged-in) visitors based on browser HTTP header

Introduction
============

The AutoRoleFromHostHeader plugin allows to assign roles to users looking
at client HTTP headers.

There is an extraction and authentication plugin included, to enable
additional roles for anonymous users. They are required since PAS does
not support roles (or properties or groups) for anonymous users.
You can disable these interfaces if only logged-in users should get
additional roles.

AutoRoleFromHostHeader furthermore provides a groups plugin interface,
allowing you to assign groups instead of roles.

Configuration
=============

The plugin is configured by editing the **Header name, regexp and roles**
property on the plugin's Properties screen. Each line represents a mapping
from an header value (using a regexp match) to one or more roles. The format
is as follows::

    http_header_name; regular expression; role[, role ...]

Caveat
======

If you have AutoRoleFromHostHeader configured for anonymous users and come
from a network matching one of its rules, you will NOT be able to log in with
an account from a higher-up user folder. This is because AutoRole authenticates
the Anonymous User which stops the lookup process.

Credits
=======

* AutoRoleFromHostHeader is not an original idea but is taken from the work
  made by *Jarn company* for the `AutoRole`__ plugin.
* Special thanks to *Mauro Amico* (mamico) for giving us the main direction.

__ http://pypi.python.org/pypi/Products.AutoRole


