.. _testing:

Testing
=======

Running tests
-------------

using runtests.py::

    $ python runtests.py
    

Coverage support
----------------

Coverage_ is a tool for measuring code coverage of Python programs. It is great
for tests and we use it as a backup - we try to cover 100% of the code used by
``django-geoprisma``. This of course does *NOT* mean that if all of the codebase
is covered by tests we can be sure there is no bug (as specification of almost
all applications requeries some unique scenarios to be tested). On the other hand
it definitely helps to track missing parts.

To run test with coverage_ support::

    $ coverage run runtests.py
    
To show the report::

    $ coverage report
    
.. note::
    You need to install coverage using:
        $ pip install coverage

.. _coverage: http://nedbatchelder.com/code/coverage/