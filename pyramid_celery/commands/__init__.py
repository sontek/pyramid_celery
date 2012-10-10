import sys
from pyramid.paster import bootstrap
from pyramid_celery.app import app

class CommandMixin(object):
    preload_options = ()

    def setup_app_from_commandline(self, argv):
        if len(argv) < 2:
            print >> sys.stderr, 'No configuration file specified.'
            sys.exit(1)

        self.config_file = argv[1]
        bootstrap(self.config_file)
        self.app = app
        return argv[:1] + argv[2:]
