#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='django-countries',
      version='1.0a2',
      description='Provides a country field for Django models.',
      author='Chris Beaven',
      author_email='smileychris@gmail.com',
      url='http://bitbucket.org/smileychris/django-countries/',
      packages=find_packages(),
      package_data={'django_countries': ['bin/*.py', 'media/*.*']},
      # titlecase PYPI is broken, copied the module directly for now (in /bin)
#      requires=['titlecase'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Framework :: Django',
      ],
)
