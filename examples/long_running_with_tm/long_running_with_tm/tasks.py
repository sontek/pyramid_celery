from celery.task import Task
from celery.task import task

import transaction

from .models import (
    DBSession,
    TaskItem,
)

import time
import random

class DeleteTask(Task):
    def run(self, task_pk):
        print 'deleting task! %s' % task_pk
        task = DBSession.query(TaskItem).filter(TaskItem.id==task_pk)[0]
        DBSession.delete(task)
        transaction.commit()

@task
def add_task(task):
    time.sleep(random.choice([2,4,6,8,10]))
    print 'creating task %s' % task
    task = TaskItem(task=task)
    DBSession.add(task)
    transaction.commit()
