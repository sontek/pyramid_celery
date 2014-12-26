from celery import Celery
from celery import signals
from celery.bin import Option
from pyramid.paster import bootstrap


celery_app = Celery()


celery_app.user_options['preload'].add(
    Option('-i', '--ini',
           help='Paste ini configuration file.'),
)


def setup_app(registry):
    if 'celery.config' in registry.settings:
        config_path = registry.settings['celery.config']
    else:
        config_path = 'celeryconfig'

    celery_app.config_from_object(config_path)
    celery_app.conf.update({'PYRAMID_REGISTRY': registry})


@signals.user_preload_options.connect
def on_preload_parsed(options, **kwargs):
    ini_location = options['ini']
    if isinstance(ini_location, tuple) and ini_location[0] == 'NO':
        print('You must provide the paste --ini argument')
        exit(-1)

    env = bootstrap(ini_location)
    registry = env['registry']
    setup_app(registry)


def includeme(config):
    setup_app(config.registry)
