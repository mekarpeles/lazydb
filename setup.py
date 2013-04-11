from distutils.core import setup
from sys import version

if version < '2.7' or version >= '3.0':
    raise NotImplemented("LazyDb requires Python 2.7.*")

setup(
    name='LazyDB',
    version='0.1.6',
    author='mek',
    author_email='michael.karpeles@gmail.com',
    packages=['lazydb'],
    scripts=[],
    url='http://pypi.python.org/pypi/LazyDB',
    license='LICENSE.txt',
    description="LazyDB is a basic wrapper around the Python shelve flatfile dbm module.",
    long_description=open('README.md').read(),
)
