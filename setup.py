#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='mdc',
      version='0.1',
      description='measurement device configuration',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: Apache 2 :: Apache License',
          'Programming Language :: Python :: 2.7',
          'Topic :: device configuration :: GUI',
      ],
      install_requires=[
          'netifaces', 'pymodbus', 'ipaddress'
      ],
      keywords='measurement device configuration with TKINTER',
      url='https://bitbucket.org/etallaou/measurement-device-configuration',
      author='Edmond Talla Ouafeu',
      author_email='tallaedd@yahoo.fr',
      license='MIT',
      packages=['mdc'],
      zip_safe=False)
