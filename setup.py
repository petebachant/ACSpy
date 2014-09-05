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
    license='GPL v3',
    description='Package for working with ACS motion controllers.',
    long_description=open('README.md').read(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4"]
)