# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='tango-articles',
    version='0.2',
    author=u'Tim Baxter',
    author_email='mail.baxter@gmail.com',
    packages=['articles'],
    url='http://github.com/tBaxter/tango-articles',
    license='LICENSE.txt',
    description='Reusable Django articles/blog content app. Can be used with or without Tango.',
    long_description=open('README.txt').read(),
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True
)
