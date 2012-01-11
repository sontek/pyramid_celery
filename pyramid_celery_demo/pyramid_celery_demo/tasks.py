from pyramid_celery import Task
from pyramid_celery import celery

import transaction

from .models import (
    DBSession,
    TaskItem,
)

class DeleteTask(Task):
    def run(self, task_id):
        print 'deleting task! %s' % task_id
        task = DBSession.query(TaskItem).filter(TaskItem.id==task_id)[0]
        DBSession.delete(task)
        transaction.commit()

@celery.task
def add_task(task):
    print 'creating task %s' % task
    task = TaskItem(task=task)
    DBSession.add(task)
    transaction.commit()
