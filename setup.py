#!/usr/bin/env python3

from setuptools import setup, find_packages
import unittest


def project_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


setup(name='pyflection',
      version="0.1",
      include_package_data=True,
      packages=find_packages(),
      test_suite="setup.project_test_suite",
      install_requires=[
          'pyvis',
      ],
      python_requires='>3.8.0')
