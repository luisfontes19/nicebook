from setuptools import find_packages, setup

# Package metadata
NAME = 'nicebook'
VERSION = '0.1.0'
DESCRIPTION = 'Simple library to generate pdf books from markdown files'
URL = 'https://github.com/luisfontes19/nicebook'
AUTHOR = 'Luis Fontes'
AUTHOR_EMAIL = ''
LICENSE = 'MIT'
KEYWORDS = ['pdf', 'markdown', 'book']

# Package dependencies
with open('requirements.txt') as f:
    INSTALL_REQUIRES = f.read().splitlines()

with open('requirements-dev.txt') as f:
    EXTRAS_REQUIRE = f.read().splitlines()

# Package setup
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    keywords=KEYWORDS,
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': [
            f'{NAME}={NAME}.cli:main',
        ],
    },
    extras_require={
        'dev': EXTRAS_REQUIRE
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ]
)
