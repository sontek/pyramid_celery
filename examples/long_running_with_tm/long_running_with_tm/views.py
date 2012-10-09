from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from .models import (
    DBSession,
    TaskItem,
)

from .tasks import (
    DeleteTask,
    add_task
)

import time

@view_config(route_name='index', renderer='long_running_with_tm:templates/tasks.mako')
def index(request):
    tasks = DBSession.query(TaskItem).all()
    return {'tasks': tasks }

@view_config(route_name='add_task')
def create_task(request):
    task_val = request.POST['task']
    add_task.delay(task_val)
    time.sleep(1)

    return HTTPFound(request.route_url('index'))

@view_config(route_name='delete_task')
def delete_task(request):
    task_pk = request.matchdict['task_pk']
    DeleteTask().delay(task_pk)
    time.sleep(1)
    return HTTPFound(request.route_url('index'))
