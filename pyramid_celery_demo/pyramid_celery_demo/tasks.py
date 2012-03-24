from celery.task import task
from celery.task import Task

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

@task
def add_task(task):
    print 'creating task %s' % task
    task = TaskItem(task=task)
    DBSession.add(task)
    transaction.commit()
