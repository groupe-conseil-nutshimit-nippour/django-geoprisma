.. _Django : https://www.djangoproject.com/
.. _GeoPrisma : http://geoprisma.org/site/index.php

Django-geoprisma
================

.. image:: https://travis-ci.org/groupe-conseil-nutshimit-nippour/django-geoprisma.svg?branch=master
    :target: https://travis-ci.org/groupe-conseil-nutshimit-nippour/django-geoprisma
    
.. image:: https://coveralls.io/repos/groupe-conseil-nutshimit-nippour/django-geoprisma/badge.png?branch=master
  :target: https://coveralls.io/r/groupe-conseil-nutshimit-nippour/django-geoprisma?branch=master

This is a Django_ version of GeoPrisma_.


Requirements
------------
Spatial database


Documentation
-------------

Online documentation is available at http://django-geoprisma.readthedocs.org/.


Installation
------------

Install Django-geoprisma ::

  pip install django-geoprisma


Add this to yours installed apps ::

  INSTALLED_APPS = (
    ...
    'modeltranslation',
    'django.contrib.gis',
    'geoprisma',
    'geoprisma.acl',
  )

**Note**
If you want to use the admin integration with django-modeltranslation,
``modeltranslation`` must be put before ``django.contrib.admin`` (only applies when using Django 1.7 or above).

Specify yours languages for django-modeltranslation ::

  gettext = lambda s: s
  LANGUAGES = (
    ('en',gettext('English')),
    ...
  )

Your template context processors must look like this ::

  TEMPLATE_CONTEXT_PROCESSORS = (
      "django.contrib.auth.context_processors.auth",
      "django.core.context_processors.debug",
      "django.core.context_processors.i18n",
      "django.core.context_processors.media",
      "django.core.context_processors.static",
      "django.core.context_processors.tz",
      "django.contrib.messages.context_processors.messages",
      "django.core.context_processors.request"
  )

Sync your database ::

  python manage.py syncdb


Load initial data ::

  python manage.py loaddata default


Now you are ready to use geoprisma.


Thanks
------

To do
