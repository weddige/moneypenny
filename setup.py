__author__ = 'Konstantin Weddige'
from setuptools import setup, find_packages

setup(
    name='Moneypenny',
    packages=find_packages(),
    version='2.0alpha2',
    description='A XMPP bot',
    author='Konstantin Weddige',
    author_email='kontakt@weddige.eu',
    url='https://github.com/weddige/moneypenny',
    license='MIT',
    scripts=('bin/moneypenny', ),
    install_requires=('sleekxmpp', 'python-seth', 'psutil', 'dnspython3', 'adventure', 'SQLAlchemy', 'PyAIML', ),
    dependency_links=('git+git://github.com/weddige/pyaiml3.git#egg=PyAIML', ),
)