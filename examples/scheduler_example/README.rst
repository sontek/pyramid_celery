Getting Started
===============================
Make sure you have a local redis-server running and then do:

.. code-block:: bash

    $ pip install -e .
    $ celery worker -A pyramid_celery.celery_app --ini development.ini -B

You can also run the worker and the beat scheduler separately:

.. code-block:: bash

    $ celery worker -A pyramid_celery.celery_app --ini development.ini
    $ celery beat -A pyramid_celery.celery_app --ini development.ini
