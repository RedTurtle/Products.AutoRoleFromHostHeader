=================================
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

Assign groups, not roles
------------------------

This plugin can be used to assign groups instead of roles if used as a *group plugin*
instead of a role plugin::

    http_header_name; regular expression; group

Caveat
======

If you have AutoRoleFromHostHeader configured for anonymous users and come
from a network matching one of its rules, you will NOT be able to log in with
an account from a higher-up user folder. This is because AutoRole authenticates
the Anonymous User which stops the lookup process.

Dependencies
============

Tested with:

* Plone 3.3
* Plone 4.1

Credits
=======

Developed with the support of `Azienda USL Ferrara`__; Azienda USL Ferrara supports
the `PloneGov initiative`__.

.. image:: http://www.ausl.fe.it/logo_ausl.gif
   :alt: Azienda USL's logo

__ http://www.ausl.fe.it/
__ http://www.plonegov.it/

Authors
=======

* This product was developed by RedTurtle Technology team.
  
  .. image:: http://www.redturtle.net/redturtle_banner.png
     :alt: RedTurtle Technology Site
     :target: http://www.redturtle.net/
  
* AutoRoleFromHostHeader is not an original idea but is taken from the work
  made by *Jarn company* for the `AutoRole`__ plugin.
* Special thanks to *Mauro Amico* (mamico) for giving us the main direction.

__ http://pypi.python.org/pypi/Products.AutoRole


