#!/usr/bin/env python
# coding=utf-8

from distutils.core import setup

setup(
    name='ACSpy',
    version='0.0.1',
    author='Pete Bachant',
    author_email='petebachant@gmail.com',
    packages=['acspy'],
    scripts=[],
    url='https://github.com/petebachant/ACSpy.git',
    license='LICENSE',
    description='Package for working with ACS motion controllers.',
    long_description=open('README.md').read()
)