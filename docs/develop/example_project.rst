.. _example-project:

Example project
===============

This example project demonstrates how to use Django-geoprisma.
You can use this example project for development or just test features.

Usage
-----

1. Clone the Django-geoprisma repo or download the archive.

2. Go to the example_project directory into the Django-geoprisma folder.

3. Install requirements ::

    $ pip install -r requirements.txt

4. You need to create a database. Don't forget to put your database configurations in settings.py ::

    $ python manage.py syncdb

5. Load default geoprisma data ::

    $ python manage.py loaddata default

6. Load example data ::

    $ python manage.py loaddata example

7. Create a superuser ::

    $ python manage.py createsuperuser

8. Run the django server ::

    $ python manage.py runserver

9. Sign in into admin with the superuser. ``http://yourserverurl/admin``

10. Enter the url ``http://yourserverurl/map/ws_example/1`` for open the geoprisma example application.
