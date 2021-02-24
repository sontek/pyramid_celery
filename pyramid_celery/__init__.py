from celery import Celery
from celery import signals
from celery import VERSION as celery_version

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
if celery_version.major >= 5:
    # Celery uses click in v5+
    from click import Option
    celery_app.user_options['preload'].add(
        Option(
            ('--ini', '-i',),
            help='Paste ini configuration file.'
        )
    )
    celery_app.user_options['preload'].add(
        Option(
            ('--ini-var',),
            help='Comma separated list of key=value to pass to ini.'
        )
    )

else:
    celery_app.user_options['preload'].add(
        add_preload_arguments
    )

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


def setup_app(app, root, request, registry, closer, ini_location):
    loader = INILoader(celery_app, ini_file=ini_location)
    celery_config = loader.read_configuration()
    #: TODO: There might be other variables requiring special handling
    boolify(
        celery_config,
        'task_always_eager',
        'enable_utc',
        'result_persistent',
    )

    if asbool(celery_config.get('use_celeryconfig', False)) is True:
        config_path = 'celeryconfig'
        celery_app.config_from_object(config_path)
    else:
        hijack_key = 'worker_hijack_root_logger'

        # TODO: Couldn't find a way with celery to do this
        hijack_logger = asbool(
            celery_config.get(hijack_key, False)
        )

        celery_config[hijack_key] = hijack_logger

        if hijack_logger is False:
            global ini_file
            ini_file = ini_location
            signals.setup_logging.connect(configure_logging)

        celery_app.config_from_object(celery_config)

    celery_app.conf.update({'PYRAMID_APP': app})
    celery_app.conf.update({'PYRAMID_ROOT': root})
    celery_app.conf.update({'PYRAMID_REQUEST': request})
    celery_app.conf.update({'PYRAMID_REGISTRY': registry})
    celery_app.conf.update({'PYRAMID_CLOSER': closer})


@signals.user_preload_options.connect
def on_preload_parsed(options, **kwargs):
    ini_location = options['ini']
    ini_vars = options['ini_var']

    if ini_location is None:
        print('You must provide the paste --ini argument')
        exit(-1)

    options = {}
    try:
        if ini_vars is not None:
            for pairs in ini_vars.split(','):
                key, value = pairs.split('=')
                options[key] = value

            env = bootstrap(ini_location, options=options)
        else:
            env = bootstrap(ini_location)
    except:  # noqa
        import traceback
        traceback.print_exc()
        exit(-1)

    registry = env['registry']
    app = env['app']
    root = env['root']
    request = env['request']
    closer = env['closer']
    setup_app(app, root, request, registry, closer, ini_location)


def configure(config, ini_location):
    setup_app(
        None,
        None,
        None,
        config.registry,
        None,
        ini_location
    )


def includeme(config):
    config.add_directive('configure_celery', configure)
