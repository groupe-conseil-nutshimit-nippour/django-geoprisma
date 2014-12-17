.. _dev_overview:

Overview
========

Here we describe the development process overview.


You want to report a bug or suggest a improvement
-------------------------------------------------

Just go to https://github.com/groupe-conseil-nutshimit-nippour/django-geoprisma/issues and create new
one.


How do I get involved ?
-----------------------

It's simple! If you want to fix a bug, extend documentation or whatever you
think is appropriate for the project and involves changes, just fork the
project at github (https://github.com/groupe-conseil-nutshimit-nippour/django-geoprisma),
create a separate branch, hack on it, publish changes at your fork and create a pull
request.

Here is a quick how to:

1. Fork a project: https://github.com/groupe-conseil-nutshimit-nippour/django-geoprisma/fork
2. Checkout project to your local machine::

       $ git clone git@github.com:YOUR_NAME/django-geoprisma.git

3. Create a new branch with name describing change you are going to work on::

       $ git checkout -b bugfix/support-for-custom-model

4. Perform changes at newly created branch. Remember to include tests (if this
   is code related change) and run test suite. See :ref:`running tests documentation
   <testing>`.
5. (Optional) Squash commits. If you have multiple commits and it doesn't make
   much sense to have them separated (and it usually makes little sense),
   please consider merging all changes into single commit. Please see
   https://help.github.com/articles/interactive-rebase if you need help with
   that.
6. Publish changes::

        $ git push origin YOUR_BRANCH_NAME

7. Create a Pull Request (https://help.github.com/articles/creating-a-pull-request).
   Usually it's as simple as opening up https://github.com/YOUR_NAME/django-geoprisma
   and clicking on review button for newly created branch. There you can make
   final review of your changes and if everything seems fine, create a Pull
   Request.