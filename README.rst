Getting Started
===============
.. image:: https://travis-ci.org/aarki/pyramid_celery.png?branch=master
           :target: https://travis-ci.org/aarki/pyramid_celery

.. image:: https://codecov.io/gh/aarki/pyramid_celery/branch/master/graph/badge.svg
           :target: https://codecov.io/gh/aarki/project-name)

Include ``pyramid_celery``, either in your ``.ini``:

.. code-block:: ini

    pyramid.includes = pyramid_celery

or, equivalently, using ``config.include``:

.. code-block:: python

    config.include('pyramid_celery')

Then you just need to tell ``pyramid_celery`` where to find the ``[celery]`` section:

.. code-block:: python

    config.configure_celery('development.ini')

Then you are free to use Celery, class-based:

.. code-block:: python

    from pyramid_celery import celery_app as app

    class AddTask(app.Task):
        def run(self, x, y):
            print x+y

or decorator-based:

.. code-block:: python

    from pyramid_celery import celery_app as app

    @app.task
    def add(x, y):
        print x+y

To get pyramid settings you may access them in ``app.conf.pyramid_registry``.

Configuration
=============

**Note on lower-case settings**: Celery version 4.0 introduced new lower-case settings and setting organization.
Examples in this documentation use the new lower case settings, but ``pyramid_celery`` continues to support old setting
names, as does Celery.

By default, ``pyramid_celery`` assumes you want to configure celery via ``.ini`` file
settings. You can do this by calling

.. code-block:: python

    config.configure_celery('development.ini')

but if you are already in the ``main`` entry point of your application, and want to use the ``.ini``
used to configure the app, you can do the following:

.. code-block:: python

    config.configure_celery(global_config['__file__'])

If you want to configure Celery from the standard ``celeryconfig`` Python file, you can specify

.. code-block:: ini

    [celery]
    use_celeryconfig = True

You can get more information on ``celeryconfig.py`` `here <http://celery.readthedocs.io/en/latest/userguide/configuration.html/>`_.

An example ``.ini`` configuration looks like this:

.. code-block:: ini

    [celery]
    broker_url = redis://localhost:1337/0
    imports = app1.tasks
              app2.tasks

    [celerybeat:task1]
    task = app1.tasks.Task1
    type = crontab
    schedule = {"minute": 0}

Scheduled/Periodic Tasks
------------------------
To use celery beat (periodic tasks), declare one ``[celerybeat:...]`` config section per task. The options are:

:``task``:
    The python task you need executed.
:``type``:
    The type of scheduling your configuration uses, one of ``crontab``, ``timedelta``, or ``integer``.
:``schedule``:
    The actual schedule for your ``type`` of configuration, parsed as JSON.
:``args``:
    Additional positional arguments, parsed as JSON.
:``kwargs``:
    Additional keyword arguments, parsed as JSON.

Example configuration:

.. code-block:: ini

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

Tasks are scheduled in UTC by default. If you want to schedule at a specific date/time in a different time zone,
use the ``timezone``
`setting <https://celery.readthedocs.io/en/latest/userguide/configuration.html#std:setting-timezone/>`_:

.. code-block:: ini

    [celery]
    timezone = US/Pacific

To get a list of available time zones, do

.. code-block:: python

    from pprint import pprint
    from pytz import all_timezones
    pprint(all_timezones)

Routing
-------
If you would like to route a task to a specific queue you can define a route
per task by declaring their ``queue`` and/or ``routing_key`` in a
``celeryroute`` section.

An example configuration for this:

.. code-block:: ini

    [celeryroute:otherapp.tasks.Task3]
    queue = slow_tasks
    routing_key = turtle

    [celeryroute:myapp.tasks.Task1]
    queue = fast_tasks

Running the worker
==================

To run the worker, use the ``celery worker`` command, and pass an additional ``--ini`` argument.

.. code-block:: bash

    celery worker -A pyramid_celery.celery_app --ini development.ini

To run the celery beat task scheduler, use the ``--beat`` option (during development), or the ``celery beat`` command
(in production).

.. code-block:: bash

    celery beat -A pyramid_celery.celery_app --ini development.ini

To expand variables in your ``.ini`` (e.g. ``%(database_username)s``), use the ``--ini-var`` option, and pass a
comma-separated list of key-value pairs.

.. code-block:: bash

    celery worker -A pyramid_celery.celery_app --ini development.ini --ini-var=database_username=sontek,database_password=OhYeah!

The ``--ini-var`` values cannot contain spaces, as this will break command-line argument parsing.

Using ``--ini-var`` multiple times is not supported, due to a bug in Celery. The issue can be tracked
`here <https://github.com/celery/celery/pull/2435/>`.

Logging
=======

If you use ``.ini`` configuration (rather than ``celeryconfig.py``), then the
logging configuration will be loaded from the ``.ini``, and the default Celery
loggers will not be used.

You most likely want to add a ``[logger_celery]`` section to your ``.ini``.

.. code-block:: ini

    [logger_celery]
    level = INFO
    handlers =
    qualname = celery

and then update your ``[loggers]`` section to include it.

If you want to use the default Celery loggers, use the ``worker_hijack_root_logger`` setting.

.. code-block:: ini

    [celery]
    worker_hijack_root_logger = True

Celery worker processes do not propagade exceptions inside tasks, swallowing them silently by default.
To fix, this, configure the ``celery.worker.job`` logger to propagate exceptions:

.. code-block:: ini

    # Make sure Celery worker doesn't silently swallow exceptions
    # See http://stackoverflow.com/a/20719461/315168
    # https://github.com/celery/celery/issues/2437
    [logger_celery_worker_job]
    level = ERROR
    handlers =
    qualname = celery.worker.job
    propagate = 1
