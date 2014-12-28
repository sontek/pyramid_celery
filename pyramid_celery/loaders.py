import datetime
import json
import celery.loaders.base
import celery.schedules
from pyramid.compat import configparser
from functools import partial


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

        if 'CELERY_IMPORTS' in config_dict:
            split_imports = config_dict['CELERY_IMPORTS'].split()
            config_dict['CELERY_IMPORTS'] = split_imports

        beat_config = {}
        beat_sections = []

        for section in self.parser.sections():
            if section.startswith('celerybeat:'):
                beat_sections.append(section)

        for section in beat_sections:
            get = partial(self.parser.get, section)
            has_option = partial(self.parser.has_option, section)

            schedule_type = get('type')
            schedule_value = json.loads(get('schedule'))

            if schedule_type == 'crontab':
                schedule = celery.schedules.crontab(**schedule_value)
            elif schedule_type == 'timedelta':
                schedule = datetime.timedelta(**schedule_value)
            elif schedule_type == 'integer':
                schedule = int(schedule_value)
            else:
                raise RuntimeError(
                    'No valid schedule type found in %s' % section
                )

            task_config = {
                'task': get('task'),
                'schedule': schedule,
            }

            if has_option('args'):
                task_config['args'] = json.loads(get('args'))

            if has_option('kwargs'):
                task_config['kwargs'] = json.loads(get('kwargs'))

            name = section.split(':', 1)[1]
            beat_config[name] = task_config

        if beat_config:
            config_dict['CELERYBEAT_SCHEDULE'] = beat_config

        return config_dict
