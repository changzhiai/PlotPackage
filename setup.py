# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 20:42:17 2021

@author: changai
"""

from setuptools import setup, find_packages

install_requires = [
    'numpy>=1.15.0',
    'scipy>=1.1.0',
    'matplotlib>=2.2.0',
]


setup(
    name="plotpackage",
    version='1.1',
    description="plot toolbox",
    url="None",
    author="Changzhi Ai",
    author_email="changai@dtu.dk",
    install_required=install_requires,
    license="MIT",
    packages=find_packages()
)