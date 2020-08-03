import datetime
import json
import celery.loaders.base
import celery.schedules
from pyramid.compat import configparser
from pyramid.exceptions import ConfigurationError
from pyramid.settings import asbool

from functools import partial


def get_any(dict_, keys, default=None):
    for key in keys:
        try:
            return dict_[key]
        except KeyError:
            pass
    return default


def set_all(dict_, keys, value):
    for key in keys:
        dict_[key] = value


def crontab(value):
    return celery.schedules.crontab(**value)


def timedelta(value):
    return datetime.timedelta(**value)


SCHEDULE_TYPE_MAP = {
    'crontab': crontab,
    'timedelta': timedelta,
    'integer': int
}


def safe_json(get, section, key):
    try:
        value = get(key)
        json_value = json.loads(value)
    except ValueError:
        msg = 'The %s=%s is not valid json in section %s' % (
            key, value, section
        )
        raise ConfigurationError(msg)

    return json_value


def get_beat_config(parser, section):
    get = partial(parser.get, section)
    has_option = partial(parser.has_option, section)

    schedule_type = get('type')
    schedule_value = safe_json(get, section, 'schedule')

    scheduler_cls = SCHEDULE_TYPE_MAP.get(schedule_type)

    if scheduler_cls is None:
        raise ConfigurationError(
            'schedule type %s in section %s is invalid' % (
                schedule_type,
                section
            )
        )

    schedule = scheduler_cls(schedule_value)

    config = {
        'task': get('task'),
        'schedule': schedule,
    }

    if has_option('args'):
        config['args'] = safe_json(get, section, 'args')

    if has_option('kwargs'):
        config['kwargs'] = safe_json(get, section, 'kwargs')

    return config


def get_route_config(parser, section):
    get = partial(parser.get, section)
    has_option = partial(parser.has_option, section)

    config = {
        'queue': get('queue')
    }

    if has_option('routing_key'):
        config['routing_key'] = get('routing_key')

    return config


class INILoader(celery.loaders.base.BaseLoader):
    def __init__(self, app, **kwargs):
        self.celery_conf = kwargs.pop('ini_file')
        self.parser = configparser.SafeConfigParser()
        self.parser.optionxform = str

        super(INILoader, self).__init__(app, **kwargs)

    def read_configuration(self, fail_silently=True):
        self.parser.read(self.celery_conf)
        config_dict = dict(self.parser.items('celery'))

        #: TODO: There might be other variables requiring special handling
        bool_settings = [
            'always_eager', 'CELERY_ALWAYS_EAGER',
            'enable_utc', 'CELERY_ENABLE_UTC',
            'result_persistent', 'CELERY_RESULT_PERSISTENT',
            'worker_hijack_root_logger', 'CELERYD_HIJACK_ROOT_LOGGER',
            'use_celeryconfig', 'USE_CELERYCONFIG',
        ]

        for setting in bool_settings:
            if setting in config_dict:
                config_dict[setting] = asbool(config_dict[setting])

        list_settings = [
            'imports', 'CELERY_IMPORTS',
            'accept_content', 'CELERY_ACCEPT_CONTENT',
        ]

        for setting in list_settings:
            if setting in config_dict:
                split_setting = config_dict[setting].split()
                config_dict[setting] = split_setting

        tuple_list_settings = [
            'admins', 'ADMINS',
        ]

        for setting in tuple_list_settings:
            if setting in config_dict:
                items = config_dict[setting].split()
                tuple_settings = [tuple(item.split(',')) for item in items]
                config_dict[setting] = tuple_settings

        dict_settings = [
            'broker_transport_options', 'BROKER_TRANSPORT_OPTIONS',
        ]

        for setting in dict_settings:
            if setting in config_dict:
                try:
                    value = json.loads(config_dict[setting])
                except ValueError:
                    value = config_dict[setting].strip().split()
                    value = dict(pair.split('=') for pair in value)
                config_dict[setting] = value

        beat_config = {}
        route_config = {}

        for section in self.parser.sections():
            if section.startswith('celerybeat:'):
                name = section.split(':', 1)[1]
                beat_config[name] = get_beat_config(self.parser, section)
            elif section.startswith('celeryroute:'):
                name = section.split(':', 1)[1]
                route_config[name] = get_route_config(self.parser, section)

        if beat_config:
            set_all(config_dict, (
                'beat_schedule', 'CELERYBEAT_SCHEDULE'), beat_config)

        if route_config:
            set_all(config_dict, (
                'task_routes', 'CELERY_ROUTES'), route_config)

        return config_dict
