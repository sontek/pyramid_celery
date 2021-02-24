from pyramid_celery import celery_app as app

import transaction

from .models import (
    DBSession,
    TaskItem,
)

import time
import random


class BaseDeleteTask(app.Task):
    """
    Base class providing methods for task model delete
    """
    def delete_method(self, task_pk):
        print('deleting task! %s' % task_pk)
        task = DBSession.query(TaskItem).filter(TaskItem.id == task_pk)[0]
        DBSession.delete(task)
        transaction.commit()


@app.task(bind=True, base=BaseDeleteTask)
def delete_task(self, task_pk):
    self.delete_method(task_pk)


@app.task
def add_task(task):
    time.sleep(random.choice([2, 4, 6, 8, 10]))
    print('creating task %s' % task)
    task = TaskItem(task=task)
    DBSession.add(task)
    transaction.commit()
