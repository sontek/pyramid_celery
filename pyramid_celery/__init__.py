from celery import Celery
from celery import signals
from celery import VERSION as celery_version
from celery.bin import Option
from pyramid.paster import bootstrap, setup_logging
from pyramid_celery.loaders import INILoader, get_any, set_all
from pyramid_celery.bootsteps import DeadlockDetection


def add_preload_arguments(parser):
    parser.add_argument(
        '-i', '--ini', default=None,
        help='Paste ini configuration file.'
    )
    parser.add_argument(
        '--ini-var', default=None, action='append',
        help='Comma separated list of key=value to pass to ini.'
    )


def make_app():
    app = Celery()
    app.steps['worker'].add(DeadlockDetection)
    if celery_version.major > 3:
        app.user_options['preload'].add(add_preload_arguments)
    else:
        app.user_options['preload'].add(Option(
            '-i', '--ini', default=None,
            help='Paste ini configuration file.'
        ))
        app.user_options['preload'].add(Option(
            '--ini-var', default=None, action='append',
            help='Comma separated list of key=value to pass to ini.'
        ))
    return app


celery_app = make_app()
ini_file = None


def configure_logging(*args, **kwargs):
    setup_logging(ini_file)


def setup_app(ini_location):
    loader = INILoader(celery_app, ini_file=ini_location)
    celery_config = loader.read_configuration()

    if get_any(celery_config, ('use_celeryconfig', 'USE_CELERYCONFIG')):
        celery_app.config_from_object('celeryconfig')
    else:
        # TODO: Couldn't find a way with celery to do this
        hijack_logger = get_any(celery_config, (
            'worker_hijack_root_logger', 'CELERYD_HIJACK_ROOT_LOGGER'), False)

        if hijack_logger is False:
            global ini_file
            ini_file = ini_location
            signals.setup_logging.connect(configure_logging)

        celery_app.config_from_object(celery_config)


def update_app(app=None, root=None, request=None, registry=None, closer=None):
    # include custom pyramid_* settings
    pyramid_conf = (
        ('pyramid_app', app),
        ('pyramid_root', root),
        ('pyramid_request', request),
        ('pyramid_registry', registry),
        ('pyramid_closer', closer),
    )
    for k, v in pyramid_conf:
        set_all(celery_app.conf, (k, k.upper()), v)


@signals.user_preload_options.connect
def on_preload_parsed(options, **kwargs):
    ini_location = options['ini']
    ini_vars = options['ini_var']

    if ini_location is None:
        print('You must provide the paste --ini argument')
        exit(-1)

    options = {}
    if ini_vars:
        for pairs in ini_vars:
            key, value = pairs.split('=')
            options[key] = value

        env = bootstrap(ini_location, options=options)
    else:
        env = bootstrap(ini_location)

    registry = env['registry']
    app = env['app']
    root = env['root']
    request = env['request']
    closer = env['closer']
    update_app(app, root, request, registry, closer)


def configure(config, ini_location):
    setup_app(ini_location)


def includeme(config):
    config.add_directive('configure_celery', configure)
