# @Author: DivineEnder
# @Date:   2016-12-22 12:12:28
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-08-13 12:06:26


"""A project to bring the alias command to Windows
See:
https://github.com/DivineEnder/Alix
"""

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

module_dir = path.abspath(path.dirname(__file__))
print(module_dir)

# Get the long description from the README file
with open(path.join(module_dir, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Alix',

    version='1.0.0',

    description='A project to bring the unix alias command to Windows',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/DivineEnder/Alix',

    # Author details
    author='DivineEnder',
    author_email='qwertydraw@gmail.com',

    license='MIT',

	# List @ https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
		# Development status
        'Development Status :: 2 - Pre-Alpha',

		# Basic identifiers
		'Natural Language :: English',
		'Operating System :: Microsoft :: Windows',
		'License :: OSI Approved :: MIT License',

		# Audience
        'Intended Audience :: Developers',

		# Topics
		'Environment :: Console',
		'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
		'Topic :: Utilities',

		# Languages
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='alix console command alias scripting',
    packages=find_packages(),
	# Requirements
    install_requires=['pickle', 'argparse', 'python-dotenv'],
	python_requires='>=3',

	entry_points={
    'console_scripts': [
        'alix=alix:main',
    ]
},
)
