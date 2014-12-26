from mock import Mock
import pytest
import mock


@pytest.mark.unit
def test_includeme_custom_config():
    from pyramid_celery import includeme
    from pyramid_celery import celery_app

    config = Mock()
    config.registry = Mock()
    basic_conf_path = 'configs.basic'
    settings = {
        'celery.config': basic_conf_path
    }
    config.registry.settings = settings
    includeme(config)

    assert celery_app.conf['BROKER_URL'] == 'redis://localhost:1337/0'


@pytest.mark.unit
def test_includeme_default():
    from pyramid_celery import includeme
    from pyramid_celery import celery_app

    config = Mock()
    config.registry = Mock()
    settings = {}
    config.registry.settings = settings

    includeme(config)
    assert celery_app.conf['BROKER_URL'] is None


@pytest.mark.unit
def test_preload_no_ini():
    from pyramid_celery import on_preload_parsed
    options = {
        'ini': ('NO', 'DEFAULT'),
    }

    with pytest.raises(SystemExit):
        on_preload_parsed(options)


@pytest.mark.unit
def test_preload_ini():
    from pyramid_celery import on_preload_parsed
    options = {
        'ini': 'dev.ini'
    }

    with mock.patch('pyramid_celery.bootstrap') as boot:
        on_preload_parsed(options)
        assert boot.called_with('dev.ini')
