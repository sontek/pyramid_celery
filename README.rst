Getting Started
=====================
Include pyramid_celery either by setting your includes in your .ini,
or by calling config.include('pyramid_celery'):

.. code-block:: python

    pyramid.includes = pyramid_celery


Now you can either use class based:

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

To get pyramid settings you may access them in app.conf['PYRAMID_REGISTRY'].

Configuration
=====================
You should use the standard `celeryconfig` python settings, you can get more
information here:

http://celery.readthedocs.org/en/latest/configuration.html


Demo
=====================
To see it all in action check out examples/long_running_with_tm, run
redis-server and then do:

.. code-block::

    $ python setup.py develop
    $ populate_long_running_with_tm development.ini
    $ pserve ./development.ini
    $ celery worker -A pyramid_celery.celery_app --ini development.ini
