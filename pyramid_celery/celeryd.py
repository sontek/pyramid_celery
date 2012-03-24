#!/usr/bin/env python
import argparse
from celery.app import default_app
from celery.bin.celeryd import WorkerCommand
from pyramid.paster import bootstrap


def main(): # pragma: no cover
    parser = argparse.ArgumentParser(description='Celery worker daemon')
    parser.add_argument('config', metavar='<ini-file>',
            help='Configuration file (and optionally section)')
    options = parser.parse_args()
    env = bootstrap(options.config)
    worker = WorkerCommand(app=default_app)
    worker.run()


if __name__ == "__main__": # pragma: no cover
    main()
