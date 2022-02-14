from setuptools import setup

setup(
    name='rfs-parts-db',
    version='1.2.5',
    description='Python-based parts database handler for Rexroth ctrlX AUTOMATION RFS platform',
    author='bostroemc',
    install_requires = ['ctrlx-datalayer', 'ctrlx_fbs', 'jsonschema'],    
    packages=['app'],
    # https://stackoverflow.com/questions/1612733/including-non-python-files-with-setup-py
    # package_data={'./': ['sampleSchema.bfbs']},
    scripts=['main.py'],
    license='Copyright (c) 2020-2021 Bosch Rexroth AG, Licensed under MIT License'
)
