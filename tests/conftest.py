import pyramid_celery
import pytest

try:
    from celery import Celery
except ImportError:
    from celery.app import Celery


@pytest.fixture(autouse=True)
def setup_celery_app(monkeypatch):
    app = Celery()
    monkeypatch.setattr(pyramid_celery, 'celery_app', app)
