from celery import Celery
from celery import signals
from celery.bin import Option

from pyramid.paster import bootstrap
from pyramid_celery.loaders import INILoader
from pyramid.settings import asbool

celery_app = Celery()


celery_app.user_options['preload'].add(
    Option('-i', '--ini',
           help='Paste ini configuration file.'),
)


def setup_app(registry, ini_location):
    loader = INILoader(celery_app, ini_file=ini_location)
    celery_config = loader.read_configuration()

    if asbool(celery_config.get('USE_CELERYCONFIG', False)) is True:
        config_path = 'celeryconfig'
        celery_app.config_from_object(config_path)
    else:
        celery_app.conf.update(celery_config)

    celery_app.conf.update({'PYRAMID_REGISTRY': registry})


@signals.user_preload_options.connect
def on_preload_parsed(options, **kwargs):
    ini_location = options['ini']

    if isinstance(ini_location, tuple) and ini_location[0] == 'NO':
        print('You must provide the paste --ini argument')
        exit(-1)

    env = bootstrap(ini_location)
    registry = env['registry']
    setup_app(registry, ini_location)


def configure(config, ini_location):
    setup_app(config.registry, ini_location)


def includeme(config):
    config.add_directive('configure_celery', configure)
