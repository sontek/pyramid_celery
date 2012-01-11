from celery import Celery

from celery.app import App

from celery.loaders import default as _default
from celery.utils import get_full_cls_name

celery = Celery()
Task = celery.create_task_cls()

def includeme(config):
    celery.config_from_object(config.registry.settings)
    celery.config = config

class PyramidLoader(_default.Loader):

    def read_configuration(self):
        config = self.app.env['registry'].settings
        settings = self.setup_settings(config)
        self.configured = True
        return settings

class Celery(App):
    flask_app = None
    loader_cls = get_full_cls_name(PyramidLoader)

    def __init__(self, env=None, *args, **kwargs):
        self.env = env
        super(Celery, self).__init__(*args, **kwargs)

    def __reduce_args__(self):
        return (self.flask_app, ) + super(Celery, self).__reduce_args__()
