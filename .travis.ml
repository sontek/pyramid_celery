language: python
sudo: false

env:
  - TOXENV=py27
  - TOXENV=py34
  - TOXENV=pypy
  - TOXENV=pypy3
  - TOXENV=flake8
  - TOXENV=cov

install:
  - travis_retry pip install tox

script:
  - travis_retry tox
