from pyramid_celery import celery_app as app
from datetime import datetime


@app.task
def get_date(*args, **kwargs):
    msg = app.conf['PYRAMID_REGISTRY'].settings['message']

    print(msg % datetime.utcnow())


@app.task
def get_date_2(*args, **kwargs):
    msg = app.conf['PYRAMID_REGISTRY'].settings['message']

    print('crontab: ' + msg % datetime.utcnow())
