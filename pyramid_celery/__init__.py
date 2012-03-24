from celery.app import default_app


def includeme(config):
    default_app.config_from_object(config.registry.settings)
    default_app.config = config
