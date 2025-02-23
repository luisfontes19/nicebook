
from setuptools import find_packages, setup

# Package metadata
NAME = 'nicebook'
VERSION = '0.1.2'
DESCRIPTION = 'Simple library to generate pdf books from markdown files'
URL = 'https://github.com/luisfontes19/nicebook'
AUTHOR = 'Luis Fontes'
AUTHOR_EMAIL = ''
LICENSE = 'MIT'
KEYWORDS = ['pdf', 'markdown', 'book']

# Package setup
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=open("README.md").read(),
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    keywords=KEYWORDS,
    packages=find_packages(),
    install_requires=[
        "marko",
        "reportlab",
        "pygments",
        "requests",
        "pyyaml",
    ],
    entry_points={
        'console_scripts': [
            f'{NAME}={NAME}.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ]
)
