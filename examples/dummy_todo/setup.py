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

setup(name='dummy_todo',
      version='0.0',
      description='dummy_todo',
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
      test_suite='dummy_todo',
      install_requires = requires,
      entry_points = """\
      [paste.app_factory]
      main = dummy_todo:main
      [console_scripts]
      populate_dummy_todo = dummy_todo.scripts.populate:main
      """,
      )

