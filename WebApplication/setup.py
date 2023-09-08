"""
Python package configuration.
"""

from setuptools import setup

setup(
    name='WebInterface',
    version='0.1.0',
    packages=['WebInterface'],
    include_package_data=True,
    install_requires=[
        'arrow',
        'bs4',
        'Flask',
        'html5validator',
        'pycodestyle',
        'pydocstyle',
        'pylint',
        'pytest',
        'requests',
    ],
    python_requires='>=3.6',
)
