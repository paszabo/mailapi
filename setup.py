import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'SQLAlchemy',
    'mysql-python',
    'pep8',
]

setup(
    name='MailApi',
    version='0.0',
    description='An interface to iredadmin',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
    ],
    author='Paul Szabo',
    author_email='paul@cupromotions.ca',
    url='',
    keywords='iredadmin iredmail email api',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='mailapi.tests',
    install_requires=requires,
    entry_points='',
)
