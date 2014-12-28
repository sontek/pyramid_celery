from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import DBSession


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings)
    config.configure_celery(global_config['__file__'])
    config.add_route('index', '/')
    config.add_route('add_task', '/add_task')
    config.add_route('delete_task', '/delete_task/{task_pk}')

    config.scan()

    return config.make_wsgi_app()
