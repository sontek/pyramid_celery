from celery import Celery
from celery import signals
from celery.bin import Option
from optparse import make_option
from pyramid.paster import bootstrap
from pyramid_celery.loaders import INILoader
from pyramid.settings import asbool

celery_app = Celery()


celery_app.user_options['preload'].add(
    make_option(
        '-i', '--ini',
        default=None,
        help='Paste ini configuration file.'),
)

celery_app.user_options['preload'].add(
    make_option(
        '--ini-var',
        default=None,
        help='Comma separated list of key=value to pass to ini'),
)


def setup_app(registry, ini_location):
    loader = INILoader(celery_app, ini_file=ini_location)
    celery_config = loader.read_configuration()

    if asbool(celery_config.get('USE_CELERYCONFIG', False)) is True:
        config_path = 'celeryconfig'
        celery_app.config_from_object(config_path)
    else:
        celery_app.config_from_object(celery_config)

    celery_app.conf.update({'PYRAMID_REGISTRY': registry})


@signals.user_preload_options.connect
def on_preload_parsed(options, **kwargs):
    ini_location = options['ini']
    ini_vars = options['ini_var']

    if ini_location is None:
        print('You must provide the paste --ini argument')
        exit(-1)

    options = {}
    if ini_vars is not None:
        for pairs in ini_vars.split(','):
            key, value = pairs.split('=')
            options[key] = value

        env = bootstrap(ini_location, options=options)
    else:
        env = bootstrap(ini_location)

    registry = env['registry']
    setup_app(registry, ini_location)


def configure(config, ini_location):
    setup_app(config.registry, ini_location)


def includeme(config):
    config.add_directive('configure_celery', configure)
