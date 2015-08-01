# -*- coding: utf-8 -*-

import codecs
import os
import re
from setuptools import setup
from sys import version


here = os.path.abspath(os.path.dirname(__file__))


if version < '2.6' or version == '3.0':
    raise NotImplementedError("LazyDb requires Python2.7.* or Python3.4")


def read(*parts):
    """Taken from pypa pip setup.py:
    intentionally *not* adding an encoding option to open, See:
    https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    """
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='LazyDB',
    version=find_version("lazydb", "__init__.py"),
    author='mek',
    author_email='michael.karpeles@gmail.com',
    packages=['lazydb'],
    scripts=[],
    url='http://pypi.python.org/pypi/LazyDB',
    license='LICENSE.txt',
    description="LazyDB is a basic wrapper around the "
        "Python shelve flatfile dbm module.",
    long_description=read('README.md')
)
