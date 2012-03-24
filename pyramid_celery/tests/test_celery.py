import unittest
from mock import Mock
from mock import patch

class TestCelery(unittest.TestCase):
    def test_includeme(self):
        from pyramid_celery import includeme
        from celery.app import default_app

        config = Mock()
        config.registry = Mock()
        settings = {'CELERY_ALWAYS_EAGER': True}
        config.registry.settings = settings
        includeme(config)

        assert default_app.config == config

    def test_includeme_with_quoted_string(self):
        from pyramid_celery import includeme
        from celery.app import default_app

        config = Mock()
        config.registry = Mock()
        settings = {
            'CELERY_ALWAYS_EAGER': True,
            'BROKER_URL': '"foo"'
        }

        config.registry.settings = settings
        includeme(config)

        assert default_app.config == config
        assert default_app.config.registry.settings['BROKER_URL'] == 'foo'

    def test_detailed_includeme(self):
        from pyramid_celery import includeme
        from celery.app import default_app

        settings = {
                'CELERY_ALWAYS_EAGER': 'true',
                'CELERYD_CONCURRENCY': '1',
                'BROKER_URL': '"redis:://localhost:6379/0"',
                'BROKER_TRANSPORT_OPTIONS': '{"foo": "bar"}',
                'ADMINS': '(("Foo Bar", "foo@bar"), ("Baz Qux", "baz@qux"))',
                'CELERYD_ETA_SCHEDULER_PRECISION': '0.1',
                'CASSANDRA_SERVERS': '["foo", "bar"]',
                'CELERY_ANNOTATIONS': '[1, 2, 3]',   # any
                'CELERY_ROUTERS': 'some.string',  # also any
                'SOME_KEY': 'SOME VALUE',
                'CELERY_IMPORTS': '("myapp.tasks", )'
        }

        config = Mock()
        config.registry = Mock()

        config.registry.settings = settings

        includeme(config)

        new_settings = default_app.config.registry.settings

        # Check conversions
        assert new_settings['CELERY_ALWAYS_EAGER'] == True
        assert new_settings['CELERYD_CONCURRENCY'] == 1
        assert new_settings['ADMINS'] == (
                ("Foo Bar", "foo@bar"),
                ("Baz Qux", "baz@qux")
        )
        assert new_settings['BROKER_TRANSPORT_OPTIONS'] == {"foo": "bar"}
        assert new_settings['CELERYD_ETA_SCHEDULER_PRECISION'] > 0.09
        assert new_settings['CELERYD_ETA_SCHEDULER_PRECISION'] < 0.11
        assert new_settings['CASSANDRA_SERVERS'] == ["foo", "bar"]
        assert new_settings['CELERY_ANNOTATIONS'] == [1, 2, 3]
        assert new_settings['CELERY_ROUTERS'] == 'some.string'
        assert new_settings['SOME_KEY'] == settings['SOME_KEY']
        assert new_settings['CELERY_IMPORTS'] == ("myapp.tasks", )

    def test_celery_quoted_values(self):
        from pyramid_celery import includeme
        from celery.app import default_app

        settings = {
                'BROKER_URL': '"redis://localhost:6379/0"',
                'BROKER_TRANSPORT_OPTIONS': '{"foo": "bar"}',
        }

        config = Mock()
        config.registry = Mock()

        config.registry.settings = settings

        includeme(config)

        new_settings = default_app.config.registry.settings

        assert new_settings['BROKER_URL'] == 'redis://localhost:6379/0'

    @patch('pyramid_celery.commands.celeryd.WorkerCommand')
    def test_celeryd(self, workercommand):
        from pyramid_celery.commands.celeryd import main

        worker = Mock()
        run = Mock()

        worker.run = run
        workercommand.return_value = worker

        settings = {'CELERY_ALWAYS_EAGER': True}
        registry = Mock()
        registry.settings = settings

        main()

#        workercommand.assert_called_with(app=celery(env))
#        bootstrap.assert_called_with('config.ini')
#        run.assert_called_once_with()
