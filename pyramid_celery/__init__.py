from celery import Celery

from celery.app import App

from celery.loaders import default as _default
from celery.utils import get_full_cls_name
from paste.deploy.converters import asbool

celery = Celery()
Task = celery.create_task_cls()


EVAL_SETTINGS = {
    'CELERYD_CONCURRENCY', 'CELERYD_PREFETCH_MULTIPLIER',
    'CELERY_TASK_RESULT_EXPIRES', 'TT_PORT', 'CELERY_REDIS_DB',
    'CELERY_REDIS_PORT', 'CELERY_REDIS_MAX_CONNECTIONS', 'BROKER_PORT',
    'BROKER_POOL_LIMIT', 'BROKER_CONNECTION_TIMEOUT',
    'BROKER_CONNECTION_RETRY', 'CELERY_TASK_RESULT_EXPIRES',
    'CELERY_MAX_CACHED_RESULTS', 'CELERYD_MAX_TASKS_PER_CHILD',
    'CELERYD_TASK_TIME_LIMIT', 'CELERYD_TASK_SOFT_TIME_LIMIT', 'EMAIL_PORT',
    'EMAIL_TIMEOUT', 'CELERYD_ETA_SCHEDULER_PRECISION', 'ADMINS',
    'CELERY_ANNOTATIONS', 'CELERY_RESULT_ENGINE_OPTIONS',
    'CELERY_CACHE_BACKEND_OPTIONS', 'CELERY_MONGODB_BACKEND_SETTINGS',
    'CASSANDRA_SERVERS', 'CELERY_ROUTES', 'BROKER_TRANSPORT_OPTIONS',
    'CELERY_TASK_PUBLISH_RETRY_POLICY', 'CELERYD_BOOT_STEPS',
}
BOOL_SETTINGS = {
    'CELERY_ENABLE_UTC', 'CELERY_RESULT_PERSISTENT',
    'CELERY_CREATE_MISSING_QUEUES', 'BROKER_USE_SSL', 'CELERY_ALWAYS_EAGER',
    'CELERY_EAGER_PROPAGATES_EXCEPTIONS', 'CELERY_IGNORE_RESULT',
    'CELERY_TRACK_STARTED', 'CELERY_TASK_PUBLISH_RETRY',
    'CELERY_DISABLE_RATE_LIMITS', 'CELERY_ACKS_LATE', 'CELERYD_FORCE_EXECV',
    'CELERY_STORE_ERRORS_EVEN_IF_IGNORED', 'CELERY_SEND_TASK_ERROR_EMAILS',
    'EMAIL_USE_SSL', 'EMAIL_USE_TLS', 'CELERY_SEND_EVENTS',
    'CELERY_SEND_TASK_SENT_EVENT', 'CELERYD_HIJACK_ROOT_LOGGER',
    'CELERYD_LOG_COLOR', 'CELERY_REDIRECT_STDOUTS',
}


def includeme(config):
    celery.config_from_object(config.registry.settings)
    celery.config = config


class PyramidLoader(_default.Loader):

    def read_configuration(self):
        config = self.app.env['registry'].settings
        config_keys = set(config.keys())
        for key in config_keys & EVAL_SETTINGS:
            config[key] = eval(config[key])
        for key in config_keys & BOOL_SETTINGS:
            config[key] = asbool(config[key])
        settings = self.setup_settings(config)
        self.configured = True
        return settings


class Celery(App):
    loader_cls = get_full_cls_name(PyramidLoader)

    def __init__(self, env=None, *args, **kwargs):
        self.env = env
        super(Celery, self).__init__(*args, **kwargs)

    def __reduce_args__(self):
        return (self.env, ) + super(Celery, self).__reduce_args__()
