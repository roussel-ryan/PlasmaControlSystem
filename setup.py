# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
	readme= f.read()

setup(
	name='ControlSystem',
	version='0.1.0',
	description='Control system for AWA plasma device',
	long_description=readme,
	author='Ryan Roussel',
	author_email='roussel@ucla.edu',
	packages=find_packages(exclude('tests', 'docs'))
)
