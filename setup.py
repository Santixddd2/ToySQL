import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.1'
PACKAGE_NAME = 'ToySQL'
AUTHOR = 'Santiago Oliva' 
AUTHOR_EMAIL = 'dogrunningsw@gmail.com' 
URL = 'https://github.com/Santixddd2' 

LICENSE = 'MIT'
DESCRIPTION = 'DBMS Library with AI models to image querys'
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') 
LONG_DESC_TYPE = "text/markdown"


INSTALL_REQUIRES = [
      'bintrees',
      'numpy',
      'tensorflow',
      'sqlparser'
      ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)