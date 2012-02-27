import unittest
from mock import Mock
from mock import patch

class TestCelery(unittest.TestCase):
    def test_includeme(self):
        from pyramid_celery import includeme
        from pyramid_celery import celery
        from pyramid_celery import Task

        config = Mock()
        config.registry = Mock()
        settings = {'CELERY_ALWAYS_EAGER': True}
        config.registry.settings = settings
        includeme(config)

        assert celery.config == config
        assert Task.app.config == config

    def test_includeme_with_quoted_string(self):
        from pyramid_celery import includeme
        from pyramid_celery import celery
        from pyramid_celery import Task

        config = Mock()
        config.registry = Mock()
        settings = {
                'CELERY_ALWAYS_EAGER': True,
                'BROKER_URL': '"foo"'
                }

        config.registry.settings = settings
        includeme(config)

        assert celery.config == config
        assert Task.app.config == config
        assert celery.config.registry.settings['BROKER_URL'] == 'foo'

    def test_celery(self):
        from pyramid_celery import Celery

        settings = {'CELERY_ALWAYS_EAGER': True}
        registry = Mock()
        registry.settings = settings

        env = {
            'registry': registry
        }

        celery = Celery(env)
        new_settings = celery.loader.read_configuration()
        reduced_args = celery.__reduce_args__()

        assert reduced_args[0] == env
        assert settings == new_settings
        assert celery.env == env


    @patch('pyramid_celery.celeryd.Celery')
    @patch('pyramid_celery.celeryd.WorkerCommand')
    @patch('pyramid_celery.celeryd.bootstrap')
    def test_celeryd(self, bootstrap, workercommand, celery):
        from pyramid_celery.celeryd import main
        worker = Mock()
        run = Mock()

        worker.run = run
        workercommand.return_value = worker

        settings = {'CELERY_ALWAYS_EAGER': True}
        registry = Mock()
        registry.settings = settings

        env = {
            'registry': registry
        }

        bootstrap.return_value = env

        main(['', 'config.ini'])

        workercommand.assert_called_with(app=celery(env))
        bootstrap.assert_called_with('config.ini')
        run.assert_called_once_with()
