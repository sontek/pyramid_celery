from celery import Celery

from celery.app import App
from celery.app.defaults import flatten
from celery.app.defaults import NAMESPACES

from celery.loaders import default as _default
from celery.utils import get_full_cls_name

celery = Celery()
Task = celery.create_task_cls()

def clean_quoted_config(config):
    # ini doesn't allow quoting, but lets support it to fit with celery
    for key,val in flatten(NAMESPACES):
        if key in config:
            if hasattr(config[key], 'replace'):
                config[key] = config[key].replace('"', '')

    return config

def includeme(config):
    cleaned_conf = clean_quoted_config(config.registry.settings)
    celery.config_from_object(cleaned_conf)
    celery.config = config

class PyramidLoader(_default.Loader):

    def read_configuration(self):
        config = self.app.env['registry'].settings
        config = clean_quoted_config(config)
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
