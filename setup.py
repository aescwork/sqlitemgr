# -*- coding: utf-8 -*-

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='sqlitemgr',
    version='1.2.5',
    description='A wrapper class for basic setup and management of an SQLite database.',
    long_description=long_description,
    url='https://github.com/aescwork/sqlitemgr',
    author='aescwork',
    author_email='aescwork@protonmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
		'Topic :: Database',
		'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='sqlitemgr sqlite development database sqlite3',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    package_data={
        'sqlitemgr': ['package_data.dat'],
    },
    entry_points={
        'console_scripts': [
            'sqlitemgr=sqlitemgr:main',
        ],
    },
)
