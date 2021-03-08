language: python
group: travis_latest
os: linux
dist: bionic

jobs:
  include:
    - python: 3.6

    - python: 3.7

    - python: 3.8


install:
  - pip install requirements.txt

script:
  - pytest