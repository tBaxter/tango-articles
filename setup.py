# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

with open('docs/requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='tango-articles',
    version='0.13.0',
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
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
