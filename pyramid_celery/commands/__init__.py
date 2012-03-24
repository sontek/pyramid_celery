import sys
from pyramid.paster import bootstrap
from celery.app import default_app


class CommandMixin(object):
    preload_options = []

    def setup_app_from_commandline(self, argv):
        if len(argv) < 2:
            print >> sys.stderr, 'No configuration file specified.'
            sys.exit(1)
        bootstrap(argv[1])
        self.app = default_app
        return argv[:1] + argv[2:]
