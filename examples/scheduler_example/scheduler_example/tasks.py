from pyramid_celery import celery_app as app
from datetime import datetime
import logging
logger = logging.getLogger(__name__)


@app.task
def get_date(*args, **kwargs):
    msg = app.conf['PYRAMID_REGISTRY'].settings['message']

    print(msg % datetime.utcnow())
    logger.info(msg % datetime.utcnow())
