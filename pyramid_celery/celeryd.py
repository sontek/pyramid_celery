#!/usr/bin/env python
import argparse
from celery.bin.celeryd import WorkerCommand
from pyramid.paster import bootstrap
from pyramid_celery import Celery


def main(): # pragma: no cover
    parser = argparse.ArgumentParser(description='Celery worker daemon')
    parser.add_argument('config', metavar='<ini-file>',
            help='Configuration file (and optionally section)')
    options = parser.parse_args()
    env = bootstrap(options.config)
    worker = WorkerCommand(app=Celery(env))
    worker.run()


if __name__ == "__main__": # pragma: no cover
    main()
