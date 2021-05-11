
from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='TheQ',
    version='0.1.0',
    description='',
    long_description=readme,
    author='Patrick Krkotic, Martin Herold',
    author_email='',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)