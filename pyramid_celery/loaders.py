import datetime
import json
import celery.loaders.base
import celery.schedules
from pyramid.compat import configparser
from pyramid.exceptions import ConfigurationError

from functools import partial


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


class INILoader(celery.loaders.base.BaseLoader):
    ConfigParser = configparser.SafeConfigParser

    def __init__(self, app, **kwargs):
        self.celery_conf = kwargs.pop('ini_file')
        self.parser = self.ConfigParser()

        super(INILoader, self).__init__(app, **kwargs)

    def read_configuration(self, fail_silently=True):
        self.parser.read(self.celery_conf)

        config_dict = {}

        for key, value in self.parser.items('celery'):
            config_dict[key.upper()] = value

        list_settings = ['CELERY_IMPORTS', 'CELERY_ACCEPT_CONTENT']

        for setting in list_settings:
            if setting in config_dict:
                split_setting = config_dict[setting].split()
                config_dict[setting] = split_setting

        beat_config = {}

        for section in self.parser.sections():
            if not section.startswith('celerybeat:'):
                continue

            name = section.split(':', 1)[1]
            beat_config[name] = get_beat_config(self.parser, section)

        if beat_config:
            config_dict['CELERYBEAT_SCHEDULE'] = beat_config

        return config_dict
