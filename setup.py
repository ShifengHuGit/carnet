#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name='carnet',
    description='VW car-net cli and library',
    author='Guillermo Pérez',
    author_email='bisho@freedreams.org',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'click',
        'requests',
        'lxml',
    ],
    entry_points={
        'console_scripts': [
            'carnet=cli.carnet:main',
        ]
    },
)
