# used by celerybeat
from datetime import timedelta
from celery.schedules import crontab

from celery.app import defaults
from celery import current_app as celery

def str_to_bool(term, table={"false": False, "no": False, "0": False,
                             "true":  True, "yes": True,  "1": True}):
    try:
        return table[term.lower()]
    except KeyError:
        raise TypeError("Can't coerce %r to type bool" % (term, ))

def clean_quoted_config(config, key):
    # ini doesn't allow quoting, but lets support it to fit with celery
    config[key] = config[key].replace('"', '')

TYPES_TO_OBJ = {
    'any': (object, None),
    'bool': (bool, str_to_bool),
    'dict': (dict, eval),
    'float': (float, float),
    'int': (int, int),
    'list': (list, eval),
    'tuple': (tuple, eval),
    'string': (str, str),
}


OPTIONS = dict(
    (key, TYPES_TO_OBJ[opt.type])
    for key, opt in defaults.flatten(defaults.NAMESPACES)
)


def convert_celery_options(config):
    """
    Converts celery options to apropriate types
    """

    for key, value in config.iteritems():
        opt_type = OPTIONS.get(key)
        if opt_type:
            if opt_type[0] == str:
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
    celery.add_defaults(config.registry.settings)
