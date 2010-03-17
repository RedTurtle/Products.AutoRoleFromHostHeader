AutoRoleFromHostHeader PAS Plugin
=================================

------------------------------------------------------------------------
Add roles to (anonymous or logged-in) visitors based on their IP address
------------------------------------------------------------------------

Introduction
============

The AutoRole plugin allows to assign roles to users from certain subnets.

There is an extraction and authentication plugin included, to enable
additional roles for anonymous users. They are required since PAS does
not support roles (or properties or groups) for anonymous users.
You can disable these interfaces if only logged-in users should get
additional roles.

AutoRole furthermore provides a groups plugin interface, allowing you to
assign groups instead of roles.

Configuration
=============

The plugin is configured by editing the **IP filter and roles** property on
the plugin's Properties screen. Each line represents a mapping from IP
network to one or more roles. The format is as follows::

  ip-address[/mask]: role[, role ...]

If ``mask`` bits are omitted, a mask of 32 is assumed.

Proxies
=======

If your Zope server is hosted behind one or more proxies, be sure to list
them in the zope.conf file using the ``trusted-proxy`` directive. AutoRole
depends on Zope's HTTPRequest to extract the client IP address, and it, in
turn, uses the ``trusted-proxy`` directive to filter out proxy IP addresses.

RAM Cache
=========

If you have PAS configured with a RAM Cache, you must add ``REMOTE_ADDR``
and ``HTTP_X_FORWARDED_FOR`` to its **REQUEST variables**.

Caveat
======

If you have AutoRole configured for anonymous users and come from a network
matching one of its rules, you will NOT be able to log in with an account from
a higher-up user folder. This is because AutoRole authenticates the Anonymous
User which stops the lookup process.

Credits
=======

Copyright 2006 Norwegian Archive, Library and Museum Authority
(http://www.abm-utvikling.no)

Copyright 2008-2009 Jarn AS (http://www.jarn.com)

AutoRole 1.0 development was sponsored by the Norwegian Archive, Library and
Museum Authority

License
=======

AutoRole is licensed under the GNU Lesser Generic Public License,
version 2.1. The complete license text can be found in file LICENSE.txt.
