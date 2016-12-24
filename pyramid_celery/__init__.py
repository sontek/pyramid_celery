from celery import Celery
from celery import signals
from celery import VERSION as celery_version
from celery.bin import Option
from pyramid.paster import bootstrap, setup_logging
from pyramid_celery.loaders import INILoader
from pyramid.settings import asbool


def add_preload_arguments(parser):
    parser.add_argument(
        '-i', '--ini', default=None,
        help='Paste ini configuration file.'
    )
    parser.add_argument(
        '--ini-var', default=None,
        help='Comma separated list of key=value to pass to ini.'
    )


celery_app = Celery()
if celery_version.major > 3:
    celery_app.user_options['preload'].add(add_preload_arguments)
else:
    celery_app.user_options['preload'].add(Option(
        '-i', '--ini', default=None,
        help='Paste ini configuration file.'
    ))
    celery_app.user_options['preload'].add(Option(
        '--ini-var', default=None,
        help='Comma separated list of key=value to pass to ini.'
    ))
ini_file = None


def boolify(config, *names):
    """Make config variables boolean.

    Celery wants ``False`` instead of ``"false"`` for CELERY_ALWAYS_EAGER.
    """

    for n in names:
        if n in config:
            config[n] = asbool(config[n])


def configure_logging(*args, **kwargs):
    setup_logging(ini_file)


def setup_app(registry, ini_location):
    loader = INILoader(celery_app, ini_file=ini_location)
    celery_config = loader.read_configuration()

    #: TODO: There might be other variables requiring special handling
    boolify(
        celery_config, 'CELERY_ALWAYS_EAGER', 'CELERY_ENABLE_UTC',
        'CELERY_RESULT_PERSISTENT'
    )

    if asbool(celery_config.get('USE_CELERYCONFIG', False)) is True:
        config_path = 'celeryconfig'
        celery_app.config_from_object(config_path)
    else:
        # TODO: Couldn't find a way with celery to do this
        hijack_logger = asbool(
            celery_config.get('CELERYD_HIJACK_ROOT_LOGGER', False)
        )

        celery_config['CELERYD_HIJACK_ROOT_LOGGER'] = hijack_logger

        if hijack_logger is False:
            global ini_file
            ini_file = ini_location
            signals.setup_logging.connect(configure_logging)

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
