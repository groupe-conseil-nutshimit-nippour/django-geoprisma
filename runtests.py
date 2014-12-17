#!/usr/bin/env python
import os
import sys
from django.conf import settings
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    app_to_test = "geoprisma"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geoprisma.tests.settings")

    if len(sys.argv) > 1:
        if sys.argv[1] == "travis":
            settings.DATABASES = {
                    'default': {
                        'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                        'NAME': 'test',                      # Or path to database file if using sqlite3.
                        # The following settings are not used with sqlite3:
                        'USER': 'postgres',
                        'PASSWORD': '',
                        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
                        'PORT': '',                      # Set to empty string for default.
                    }
            }

    execute_from_command_line([sys.argv[0], "test", app_to_test])
