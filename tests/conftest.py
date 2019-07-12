import pyramid_celery
import pytest


@pytest.fixture(autouse=True)
def setup_celery_app(monkeypatch):
    # use a fresh app instance for each test
    app = pyramid_celery.make_app()
    monkeypatch.setattr(pyramid_celery, 'celery_app', app)
