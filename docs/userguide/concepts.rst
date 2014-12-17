.. _concepts:

Concepts
========

In this section, you will learn more about the terms and words commonly used in ``Django-geoprisma``.


Resource
--------

A Resource is associated to a unique set of data, but it can have many different
Web Services serving it in different ways. For example, a Resources named GMap_Roads
could have its data served by many different kind of servers.

The Access Control on Resources is managed by the ACL.


DataStore
---------

It's the equivalent of a layer of a server, i.e. a LAYER of a mapfile (MapServer),
or a layer in a configuration file (FeatureServer, TileCache), etc.
DataStores are linked to a single Service.


Service
-------

A Service is a GeoSpacial Web Server, like WMS.

Here's a list of the current Service available in ``Django-geoprisma``:

- WMS
- FeatureServer
- MapCache
- MapServer
- GYMO (Google, Yahoo, Microsoft, OpenStreetMap)
- File
- WFS
- HTTPRequest


Widget
------

A widget is a feature of the UI application.
Each widget can be associated to one or more Resources.
The Resource has to have the according service defined by the Widget
ServiceType to be able to use the widget properly.

**For example :**
A QueryOnClick widget that has Action:read and ServiceType:WMS could be added to a Resource
if that Resource has a WMS Service configured and would be added to the UI
if the User has the read Permission to the related Resource.


ACL
---

ACL stands for Access Control List. It's the application responsible
of managing the Permissions, Actions, Roles and Resources in ``Django-geoprisma``.


Proxy
-----

The Proxy of ``Django-geoprisma`` is the only point of entry for any queries made.
For example, if we would want to make a WMS 'GetMap' query to a
WMS Service that is defined in the Config, it must be made through the Proxy.


Template
--------

A Template is a HTML file used as a UI skeleton.
It has a list supported widgets and where to draw them.
It uses Django's template language and the ExtJS API.


MapContext
----------

A MapContext is basically a list of Resource inside a specific geospatial context, resulting in a map.


Application
-----------

An Application consist of a list of Widget and a specific Template, resulting
in a complete webmapping application, but without any data layer.


Session
-------
Combining a MapContext with a Application results in a complete webmapping application
(with the Application defined widgets) using and having data layers in it (from the MapContext defined resources).
This combinaison is called a Session.



