from distutils.core import setup

setup(
    name='LazyDB',
    version='0.1.4',
    author='mek',
    author_email='michael.karpeles@gmail.com',
    packages=['lazydb', 'lazydb.test'],
    scripts=[],
    url='http://pypi.python.org/pypi/LazyDB',
    license='LICENSE.txt',
    description="LazyDB is a basic wrapper around the Python shelve flatfile dbm module.",
    long_description=open('README.txt').read(),
)
