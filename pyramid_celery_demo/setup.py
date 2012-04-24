from setuptools import setup, find_packages

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'redis',
    ]

setup(name='pyramid_celery_demo',
      version='0.0',
      description='pyramid_celery_demo',
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
      test_suite='pyramid_celery_demo',
      install_requires = requires,
      entry_points = """\
      [paste.app_factory]
      main = pyramid_celery_demo:main
      [console_scripts]
      populate_pyramid_celery_demo = pyramid_celery_demo.scripts.populate:main
      """,
      )

