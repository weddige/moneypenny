__author__ = 'Konstantin Weddige'
from setuptools import setup, find_packages

setup(
    name='Moneypenny',
    packages=find_packages(),
    version='2.0alpha1',
    description='A XMPP bot',
    author='Konstantin Weddige',
    license='MIT',
    scripts=('bin/moneypenny', )
)