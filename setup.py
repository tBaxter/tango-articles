# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

with open('docs/requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='tango-articles',
    version='0.4',
    author=u'Tim Baxter',
    author_email='mail.baxter@gmail.com',
    url='http://github.com/tBaxter/tango-articles',
    license='LICENSE.txt',
    description='Reusable Django articles/blog content app. Can be used with or without Tango.',
    long_description=open('README.md').read(),
    packages=find_packages(),
    install_requires=required,
    zip_safe=False,
    include_package_data=True,
    dependency_links = ['http://github.com/tBaxter/tango-shared-core/tarball/master#egg=tango-shared-0.5']
)
