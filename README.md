Getting Started
=====================
Include pyramid_celery either by setting your includes in your .ini,
or by calling config.include('pyramid_celery').

``` python
    pyramid.includes = pyramid_celery
```

Now you can either use class based:

``` python
from pyramid_celery import Task
from eventq.managers.settings import UserPermissionManager

class AddTask(Task):
    def run(self, x, y):
        print x+y
```

or decorator based:

``` python
from pyramid_celery import celery

@celery.task
def add(x, y):
    print x+y
```

Configuration
=====================
All standard celery configuration options will work. Check out http://ask.github.com/celery/configuration.html
