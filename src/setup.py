__author__="Matej Urbas [matej.urbas@gmail.com]"
__date__ ="$25-Sep-2010 21:36:10$"

from setuptools import setup,find_packages

setup (
  name = 'HomeLib',
  version = '0.1',
  packages = find_packages(),

  install_requires=["Mercurial>=1.6.3"],

  author = 'Matej Urbas',
  author_email = 'matej@urbas.si',

  summary = 'A library for configuration and management of a personal environment.',
  url = 'http://urbas.si/',
  license = 'MIT',
  long_description= 'A library for configuration and management of a personal environment.',
)