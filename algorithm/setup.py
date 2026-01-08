"""
Algorithm for Resonator Parameter Extraction from
Symmetrical and Asymmetrical Transmission Responses

Authors:
    Patrick Krkotic
    Queralt Gallardo
    Nikki Tagdulang
    Montse Pont
    Joan M. O'Callaghan

Contributors:
    Agustin Gomez Mansilla
    Martin Herold
    Tamas Madarasz

Contact:
    arpe-edu@outlook.de

Original Publication:
    2021

Version History:
    v1.0.0  – Initial release (Python 3.7.7) - 2021
    v2.0.0  – New interface and updated to Python 3.11.9 - 2023
    v2.1.0  – Novel routine for over and undercoupling, refactoring and clean-up, and update to Python 3.12.10 - 2026

Citation:
    Please cite the original 2021 publication when using this code.
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