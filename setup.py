#!/usr/bin/env python
import os
from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='ibl-request-router',
    version='0.2.2',
    packages=find_packages(),
    include_package_data=True,
    description='Request router',
    url='https://gitlab.com/deeplms/ibl-request-router',
    author='IBL Studios',
    author_email='ibl@ibl.ibl',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP'
    ],
)
