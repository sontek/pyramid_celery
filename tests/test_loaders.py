import pytest
import os

here = os.path.dirname(__name__)


@pytest.mark.unit
def test_basic_ini():
    from pyramid_celery import celery_app
    from pyramid_celery.loaders import INILoader
    from celery.schedules import crontab
    import datetime

    ini_path = os.path.join(here, 'tests/configs/dev.ini')
    loader = INILoader(celery_app, ini_file=ini_path)
    result = loader.read_configuration()
    schedule = result['CELERYBEAT_SCHEDULE']

    assert result['BROKER_URL'] == 'redis://localhost:1337/0'
    assert result['ADMINS'] == [
        ('john', 'john@initrode.example'),
        ('exceptions', 'exceptions@majortech.example')]
    assert schedule['task1']['task'] == 'myapp.tasks.Task1'
    assert schedule['task2']['task'] == 'myapp.tasks.Task2'
    assert schedule['task3']['task'] == 'otherapp.tasks.Task3'
    assert schedule['task4']['task'] == 'myapp.tasks.Task4'
    assert isinstance(schedule['task1']['schedule'], crontab)
    assert isinstance(schedule['task2']['schedule'], datetime.timedelta)
    assert isinstance(schedule['task4']['schedule'], int)
    assert schedule['task2']['args'] == [16, 16]
    assert schedule['task3']['kwargs'] == {"boom": "shaka"}


@pytest.mark.unit
def test_bad_ini():
    from pyramid_celery import celery_app
    from pyramid_celery.loaders import INILoader
    from pyramid.exceptions import ConfigurationError
    ini_path = os.path.join(here, 'tests/configs/bad.ini')
    loader = INILoader(celery_app, ini_file=ini_path)

    with pytest.raises(ConfigurationError) as e:
        loader.read_configuration()

    msg = 'schedule type sundial in section celerybeat:task1 is invalid'
    assert str(e.value) == msg


@pytest.mark.unit
def test_bad_json():
    from pyramid_celery import celery_app
    from pyramid_celery.loaders import INILoader
    from pyramid.exceptions import ConfigurationError
    ini_path = os.path.join(here, 'tests/configs/bad_json.ini')
    loader = INILoader(celery_app, ini_file=ini_path)

    with pytest.raises(ConfigurationError) as e:
        loader.read_configuration()

    msg = (
        'The schedule={"seconds": 60*60*60} is not valid json in section '
        'celerybeat:task1'
    )

    assert str(e.value) == msg


@pytest.mark.unit
def test_celery_routing():
    from pyramid_celery import celery_app
    from pyramid_celery.loaders import INILoader

    ini_path = os.path.join(here, 'tests/configs/routing.ini')
    loader = INILoader(celery_app, ini_file=ini_path)
    result = loader.read_configuration()
    routes = result['CELERY_ROUTES']

    assert result['BROKER_URL'] == 'redis://localhost:1337/0'
    assert routes['myapp.tasks.Task1']['queue'] == 'fast_tasks'
    assert routes['otherapp.tasks.Task3']['queue'] == 'slow_tasks'
