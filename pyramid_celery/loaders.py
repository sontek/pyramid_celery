import datetime
import json
import celery.loaders.base
import celery.schedules
from pyramid.compat import configparser


class INILoader(celery.loaders.base.BaseLoader):

    def __init__(self, app, **kwargs):
        self.celery_conf = kwargs.pop('ini_file')
        super(INILoader, self).__init__(app, **kwargs)

    def read_configuration(self, fail_silently=True):
        config = configparser.SafeConfigParser()
        config.read(self.celery_conf)

        # Read main celery config
        config_dict = dict(
            [(key.upper(), value) for key, value in config.items('celery')]
        )

        # Conversions
        if 'CELERY_IMPORTS' in config_dict:
            split_imports = config_dict['CELERY_IMPORTS'].split(',')
            config_dict['CELERY_IMPORTS'] = split_imports

        # Explicitly tell celery to not hijack root logger since we
        # allow configuring our own own logger
        # config_dict['CELERYD_HIJACK_ROOT_LOGGER'] = False

        # Read celery beat config
        beat_config = {}
        beat_sections = [
            c for c in config.sections() if c.startswith('celerybeat:')
        ]

        for section in beat_sections:
            schedule_type = config.get(section, 'type')
            schedule_value = json.loads(config.get(section, 'schedule'))
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
                'task': config.get(section, 'task'),
                'schedule': schedule,
            }

            if config.has_option(section, 'args'):
                task_config['args'] = json.loads(config.get(section, 'args'))

            if config.has_option(section, 'kwargs'):
                task_config['kwargs'] = json.loads(
                    config.get(section, 'kwargs')
                )

            name = section.split(':', 1)[1]
            beat_config[name] = task_config

        config_dict['CELERYBEAT_SCHEDULE'] = beat_config

        return config_dict
