import os, sys
try:
    from setuptools import setup, find_packages
    use_setuptools = True
except ImportError:
    from distutils.core import setup
    use_setuptools = False

try:
    with open('README.rst', 'rt') as readme:
        description = '\n' + readme.read()
except IOError:
    # maybe running setup.py from some other dir
    description = ''

install_requires = [
    'pyserial>=2.7',
    'twisted>=13.0.0'
]

setup(
    name="flock",
    version='0.3.0',
    url='https://github.com/',
    license='MIT',
    description="Smart home library for python",
    long_description=description,
    author='Romain Picard',
    author_email='romain.picard@oakbits.com',
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
    ],
    scripts=['flockd.py', 'flockctl'],
)
