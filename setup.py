from setuptools import setup

setup(
    name='rfs-parts-db',
    version='1.3.9',
    description='Python-based parts database handler for Rexroth ctrlX AUTOMATION RFS platform',
    author='bostroemc',
    install_requires = ['ctrlx-datalayer', 'ctrlx_fbs', 'jsonschema'],    
    packages=['app'],
    scripts=['main.py'],
    license='Copyright (c) 2020-2022 Bosch Rexroth AG, Licensed under MIT License'
)
