NB: I have made minimal patches to make this (appear to) work on Python 3.x and Pyramid 1.5. I have not extensively tested these changes, but celery workers and celerybeat both start up and start working. 

Getting Started
=====================
Include pyramid_celery either by setting your includes in your .ini,
or by calling config.include('pyramid_celery').

``` python
    pyramid.includes = pyramid_celery
```

Now you can either use class based:

``` python
from celery.task import task
from celery.task import Task

@task
class AddTask(Task):
    def run(self, x, y):
        print x+y
```

or decorator based:

``` python
from celery.task import task

@task
def add(x, y):
    print x+y
```

Configuration
=====================
All standard celery configuration options will work. Check out http://ask.github.com/celery/configuration.html

Demo
=====================
To see it all in action check out pyramid_celery_demo, run rabbitmq-server and then do:

``` python
$ python setup.py develop
$ populate_pyramid_celery_demo ./development.ini
$ pserve ./development.ini
$ pcelery ./development.ini worker
```

If you are using celery < 3.1 use  older celery command lines binding.
``` python
pceleryd development.ini
```
