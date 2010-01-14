#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='django-countries-2',
      version='1.0',
      author='Chris Beaven',
      author_email='smileychris@gmail.com',
      packages=find_packages(),
      package_data={'django_countries': ['bin/*.py', 'media/*.*']},
      # titlecase PYPI is broken, copied the module directly for now (in /bin)
#      requires=['titlecase']
)

