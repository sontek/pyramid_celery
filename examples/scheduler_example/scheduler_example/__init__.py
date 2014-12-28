from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['message'] = "The current date is %s"
    config = Configurator(settings=settings)
    config.scan()
    return config.make_wsgi_app()
