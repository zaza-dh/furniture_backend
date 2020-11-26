#!//usr/bin/env python3.6

import os
from setuptools import setup


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="ikea_backend",
    install_requires=required
)
