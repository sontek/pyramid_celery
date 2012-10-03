import os
import sys
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = ['pyramid', 'celery']
if sys.version_info < (2, 7):
    requires.append('argparse')

setup(name='pyramid_celery',
      version='1.3',
      description='Celery integration with pyramid',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      author='John Anderson',
      author_email='sontek@gmail.com',
      url='https://github.com/sontek/pyramid_celery',
      keywords='paste pyramid celery message queue amqp job task distributed',
      license='BSD',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires + ['pytest', 'mock'],
      test_suite="pyramid_celery",
      entry_points = """\
        [console_scripts]
        pceleryd = pyramid_celery.commands.celeryd:main
        pceleryctl = pyramid_celery.commands.celeryctl:main
        pcelerybeat = pyramid_celery.commands.celerybeat:main
        pceleryev = pyramid_celery.commands.celeryev:main
      """,
      )
