import pyramid_celery
from celery import Celery


def pytest_runtest_setup(item):
    pyramid_celery.celery_app = Celery()
