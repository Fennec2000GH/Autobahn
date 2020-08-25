
from setuptools import find_packages, setup

setup(
    name='Flite',
    packages=find_packages(include='Flite-1.0.0'),
    version='1.0.0',
    description='Fast and efficient linear data structure library',
    author='Caijun Qin',
    license='MIT',
    install_requires=['multimethod==1.4', 'numpy==1.19.0'],
    setup_requires=['pytest-runner==5.2'],
    tests_require=['pytest==5.4.3'],
    test_suite=['tests']
)
