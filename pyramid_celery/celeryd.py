#!/usr/bin/env python
import os
import sys
from celery.bin.celeryd import WorkerCommand
from pyramid.paster import bootstrap
from pyramid_celery import Celery

def usage(argv):# pragma: no cover 
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd)) 
    sys.exit(1)

def main(argv=sys.argv): # pragma: no cover
    if len(argv) != 2:
        usage(argv)

    config_uri = argv[1]

    env = bootstrap(config_uri)

    worker = WorkerCommand(app=Celery(env))
    worker.run()

if __name__ == "__main__": # pragma: no cover
    main()
