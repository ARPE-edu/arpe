"""
Algorithm for Resonator Parameter Extraction from Symmetrical and Asymmetrical Transmission Responses
by Patrick Krkotic, Queralt Gallardo, Nikki Tagdulang, Montse Pont and Joan M. O'Callaghan, 2021

Code written by Patrick Krkotic and Queralt Gallardo
arpe-edu@outlook.de

Version 1.0.0
Contributors:

Developed on Python 3.7.7
"""

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='TheQ',
    version='1.0.0',
    description='',
    long_description=readme,
    author='Patrick Krkotic',
    author_email='arpe-edu@outlook.com',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)