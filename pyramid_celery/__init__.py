from celery.app import default_app
from celery.app import defaults


def clean_quoted_config(config, key):
    # ini doesn't allow quoting, but lets support it to fit with celery
    config[key] = config[key].replace('"', '')

TYPES_TO_OBJ = {
    'any': (object, None),
    'bool': (bool, defaults.str_to_bool),
    'dict': (dict, eval),
    'float': (float, float),
    'int': (int, int),
    'list': (list, eval),
    'tuple': (tuple, eval),
    'string': (str, None),
}


OPTIONS = {
    key: TYPES_TO_OBJ[opt.type]
    for key, opt in defaults.flatten(defaults.NAMESPACES)
#    if opt.type != 'string'
}


def convert_celery_options(config):
    """
    Converts celery options to apropriate types
    """

    for key, value in config.iteritems():
        opt_type = OPTIONS.get(key)

        if opt_type:
            if opt_type == 'string' or key == 'BROKER_URL':
                clean_quoted_config(config, key)
            elif opt_type[0] is object:
                try:
                    config[key] = eval(value)
                except:
                    pass  # any can be anything; even a string
            elif not isinstance(value, opt_type[0]):
                config[key] = opt_type[1](value)

def includeme(config):
    convert_celery_options(config.registry.settings)
    default_app.config_from_object(config.registry.settings)
    default_app.config = config
