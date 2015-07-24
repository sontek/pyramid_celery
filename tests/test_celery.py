import pytest
import mock


@pytest.mark.unit
def test_includeme_custom_config():
    from pyramid_celery import includeme
    from pyramid_celery import celery_app
    from pyramid import testing
    from pyramid.registry import Registry
    config = testing.setUp()
    config.registry = Registry()
    config.registry.settings = {}
    includeme(config)
    config.configure_celery('tests/configs/dev.ini')
    assert celery_app.conf['BROKER_URL'] == 'redis://localhost:1337/0'
    assert celery_app.conf['CELERY_TIMEZONE'] == 'America/Los_Angeles'


@pytest.mark.unit
def test_includeme_default():
    from pyramid_celery import includeme
    from pyramid_celery import celery_app
    from pyramid import testing
    from pyramid.registry import Registry
    config = testing.setUp()
    config.registry = Registry()
    config.registry.settings = {}

    includeme(config)
    assert celery_app.conf['BROKER_URL'] is None


@pytest.mark.unit
def test_includeme_use_celeryconfig():
    from pyramid_celery import includeme
    from pyramid_celery import celery_app
    from pyramid import testing
    from pyramid.registry import Registry
    config = testing.setUp()
    config.registry = Registry()
    config.registry.settings = {}

    includeme(config)
    config.configure_celery('tests/configs/useceleryconfig.ini')

    assert celery_app.conf['BROKER_URL'] == 'redis://localhost:1337/0'


@pytest.mark.unit
def test_preload_no_ini():
    from pyramid_celery import on_preload_parsed
    options = {
        'ini': None,
        'ini_var': None,
    }

    with pytest.raises(SystemExit):
        on_preload_parsed(options)


@pytest.mark.unit
def test_preload_ini():
    from pyramid_celery import on_preload_parsed
    options = {
        'ini': 'tests/configs/dev.ini',
        'ini_var': None,
    }

    with mock.patch('pyramid_celery.bootstrap') as boot:
        on_preload_parsed(options)
        assert boot.called_with('dev.ini')


@pytest.mark.unit
def test_celery_imports():
    from pyramid_celery import includeme, celery_app
    from pyramid import testing
    from pyramid.registry import Registry
    config = testing.setUp()
    config.registry = Registry()
    config.registry.settings = {}

    includeme(config)
    config.configure_celery('tests/configs/imports.ini')

    assert celery_app.conf['CELERY_IMPORTS'] == [
        'myapp.tasks',
        'otherapp.tasks'
    ]


@pytest.mark.unit
def test_preload_with_ini_vars():
    from pyramid_celery import on_preload_parsed
    options = {
        'ini': 'tests/configs/dev.ini',
        'ini_var': 'database=foo,password=bar',
    }

    with mock.patch('pyramid_celery.bootstrap') as boot:
        on_preload_parsed(options)
        expected_vars = {'database': 'foo', 'password': 'bar'}
        assert boot.called_with('dev.ini', expected_vars)


@pytest.mark.unit
def test_ini_logging():
    from celery import signals
    from pyramid_celery import includeme
    from pyramid import testing
    from pyramid.registry import Registry
    config = testing.setUp()
    config.registry = Registry()
    config.registry.settings = {}
    includeme(config)
    config.configure_celery('tests/configs/dev.ini')

    with mock.patch('pyramid_celery.setup_logging') as setup_logging:
        signals.setup_logging.send(
            sender=None, loglevel='INFO', logfile=None,
            format='', colorize=False,
        )

    assert setup_logging.called_with('tests/configs/dev.ini')


@pytest.mark.unit
def test_celery_accept_content():
    from pyramid_celery import includeme, celery_app
    from pyramid import testing
    from pyramid.registry import Registry
    config = testing.setUp()
    config.registry = Registry()
    config.registry.settings = {}

    includeme(config)
    config.configure_celery('tests/configs/dev.ini')

    assert celery_app.conf['CELERY_ACCEPT_CONTENT'] == [
        'json',
        'xml'
    ]
