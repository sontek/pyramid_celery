#!/usr/bin/env python
# -*0 coding: utf-8 -*-
import sys, os

try:
    from setuptools import setup, find_packages, Command
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages, Command

version = '1.0'

setup(name='pyramid_celery',
      version=version,
      description="Celery integration with Pyramid.",
      long_description=""" """,
      classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pyramid",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: System :: Distributed Computing"
        ],
      keywords='paste pyramid celery message queue amqp job task distributed',
      author='John Anderson',
      author_email='sontek@gmail.com',
      url='https://github.com/sontek/pyramid_celery',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
        "pyramid",
        "celery",
      ],
      entry_points="""
      # -*- Entry points: -*-
      [paste.global_paster_command]
      celeryd=pyramid_celery.commands:CeleryDaemonCommand
      celerybeat=pyramid_celery.commands:CeleryBeatCommand
      camqadm=pyramid_celery.commands:CAMQPAdminCommand
      celeryev=pyramid_celery.commands:CeleryEventCommand
      """,
      )
