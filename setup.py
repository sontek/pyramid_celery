import os
import sys
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = ['pyramid', 'celery']

if sys.version_info < (2, 7):
    requires.append('argparse')


setup(name='pyramid_celery',
      version='3.0.0',
      description='Celery integration with pyramid',
      long_description=README + "\n" + CHANGES,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: Unix",
          "Operating System :: POSIX",
          "Operating System :: Microsoft :: Windows",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
      ],
      author='John Anderson',
      author_email='sontek@gmail.com',
      url='https://github.com/sontek/pyramid_celery',
      keywords='paste pyramid celery message queue amqp job task distributed',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires + ['pytest', 'mock'],
      test_suite="pyramid_celery",
      )
