Getting Started
=====================
.. image:: https://travis-ci.org/sontek/pyramid_celery.png?branch=master
           :target: https://travis-ci.org/sontek/pyramid_celery

.. image:: https://coveralls.io/repos/sontek/pyramid_celery/badge.png?branch=master
           :target: https://coveralls.io/r/sontek/pyramid_celery?branch=master

.. image:: https://img.shields.io/pypi/v/pyramid_celery.svg
           :target: https://pypi.python.org/pypi/pyramid_celery

Include pyramid_celery either by setting your includes in your .ini,
or by calling ``config.include('pyramid_celery')``:

.. code-block:: ini

    pyramid.includes = pyramid_celery


Then you just need to tell **pyramid_celery** what ini file your **[celery]**
section is in:

.. code-block:: python

    config.configure_celery('development.ini')

Then you are free to use celery, for example class based:

.. code-block:: python

    from pyramid_celery import celery_app as app

    class AddTask(app.Task):
        def run(self, x, y):
            print x+y

or decorator based:

.. code-block:: python

    from pyramid_celery import celery_app as app

    @app.task
    def add(x, y):
        print x+y

To get pyramid settings you may access them in ``app.conf['PYRAMID_REGISTRY']``.

Configuration
=====================
By default **pyramid_celery** assumes you want to configure celery via an ini
settings. You can do this by calling **config.configure_celery('development.ini')**
but if you are already in the **main** of your application and want to use the ini
used to configure the app you can do the following:

.. code-block:: python

    config.configure_celery(global_config['__file__'])

If you want to use the standard **celeryconfig** python file you can set the
**USE_CELERYCONFIG = True** like this:

.. code-block:: ini

    [celery]
    USE_CELERYCONFIG = True

You can get more information for celeryconfig.py here:

http://celery.readthedocs.org/en/latest/configuration.html

An example ini configuration looks like this:

.. code-block:: ini

    [celery]
    BROKER_URL = redis://localhost:1337/0
    CELERY_IMPORTS = app1.tasks
                     app2.tasks

    [celerybeat:task1]
    task = app1.tasks.Task1
    type = crontab
    schedule = {"minute": 0}

    [celerybeat:task2]
    task = app1.tasks.Task2
    type = timedelta
    schedule = {"seconds": 30}
    args = [16, 16]

    [celerybeat:task3]
    task = app2.tasks.Task1
    type = crontab
    schedule = {"hour": 0, "minute": 0}
    kwargs = {"boom": "shaka"}

    [celerybeat:task4]
    task = myapp.tasks.Task4
    type = integer
    schedule = 30

Running the worker
=============================
To run the worker we just use the standard celery command with an additional
argument:

.. code-block:: bash

    celery worker -A pyramid_celery.celery_app --ini development.ini

If you've defined variables in your .ini like %(database_username)s you can use
the *--ini-var* argument, which is a comma separated list of key value pairs:

.. code-block:: bash

    celery worker -A pyramid_celery.celery_app --ini development.ini --ini-var=database_username=sontek,database_password=OhYeah!

The values in *ini-var* cannot have spaces in them, this will break celery's
parser.

The reason it is a csv instead of using *--ini-var* multiple times is because of
a bug in celery itself.  When they fix the bug we will re-work the API. Ticket
is here:

https://github.com/celery/celery/pull/2435

If you use celerybeat scheduler you need to run with the *-B* flag to run
beat and worker at the same time or you can launch it separately like this:

.. code-block:: bash

    celery beat -A pyramid_celery.celery_app --ini development.ini

Logging
=====================
If you use the **.ini** configuration (i.e don't use celeryconfig.py) then the
logging configuration will be loaded from the .ini and will not use the default
celery loggers.

If you want use the default celery loggers then you can set
**CELERYD_HIJACK_ROOT_LOGGER=True** in the [celery] section of your .ini

Demo
=====================
To see it all in action check out examples/long_running_with_tm, run
redis-server and then do:

.. code-block:: bash

    $ python setup.py develop
    $ populate_long_running_with_tm development.ini
    $ pserve ./development.ini
    $ celery worker -A pyramid_celery.celery_app --ini development.ini
