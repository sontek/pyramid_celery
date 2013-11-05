from setuptools import setup, find_packages

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'pyramid_celery',
    'zope.sqlalchemy',
    'redis',
    'psycopg2'
]

setup(name='long_running_with_tm',
      version='0.0',
      description='long_running_with_tm',
      long_description="",
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='long_running_with_tm',
      install_requires = requires,
      entry_points = """\
      [paste.app_factory]
      main = long_running_with_tm:main
      [console_scripts]
      populate_long_running_with_tm = long_running_with_tm.scripts.populate:main
      """,
      )

