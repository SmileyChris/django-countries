#!/usr/bin/env python
import os
import sys
from setuptools import setup, find_packages

if sys.version_info <= (3, ):
    from codecs import open

def long_description():
    """
    Build the long description from a README file located in the same directory
    as this module.
    """
    base_path = os.path.dirname(os.path.realpath(__file__))
    readme = open(os.path.join(base_path, 'README.rst'),
                  encoding='utf-8')
    try:
        return readme.read()
    finally:
        readme.close()


setup(
    name='django-countries',
    version='2.1.2',
    description='Provides a country field for Django models.',
    long_description=long_description(),
    author='Chris Beaven',
    author_email='smileychris@gmail.com',
    url='https://github.com/SmileyChris/django-countries/',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Framework :: Django',
    ],
)
