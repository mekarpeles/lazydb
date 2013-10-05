from distutils.core import setup
from sys import version
import os

if version < '2.6' or version >= '3.0':
    raise NotImplementedError("LazyDb requires either Python 2.6.* or 2.7.*")

setup(
    name='LazyDB',
    version='0.1.66',
    author='mek',
    author_email='michael.karpeles@gmail.com',
    packages=['lazydb'],
    scripts=[],
    url='http://pypi.python.org/pypi/LazyDB',
    license='LICENSE.txt',
    description="LazyDB is a basic wrapper around the Python shelve flatfile dbm module.",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
)
