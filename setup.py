#!/usr/bin/env python
from glob import glob
from os.path import basename, splitext
import os
from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='ibl-request-router',
    version='0.2.5',
    packages=find_packages('src'),
    install_requires=['requests-mock'],
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    description='Request router',
    url='https://gitlab.com/deeplms/ibl-request-router',
    author='IBL Studios',
    author_email='ibl@ibl.ibl',
    entry_points={
        'lms.djangoapp': [
            'ibl_request_router = ibl_request_router.apps:RequestRouterConfig',
        ],
        'cms.djangoapp': [
            'ibl_request_router = ibl_request_router.apps:RequestRouterConfig',
        ]
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP'
    ],
)
