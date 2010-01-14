#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='django-countries',
      version='1.0a1',
      description="Python Port of John Gruber's titlecase.pl",
      author='Chris Beaven',
      author_email='smileychris@gmail.com',
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
