#!/usr/bin/env python

from setuptools import setup, find_packages

# setup information
setup(name = 'twine',
      description = 'An implementation of twill based on spynner',
      author = 'Joshua Curl, C. Titus Brown, and Ben R. Taylor',
      author_email = 'curljosh@msu.edu',
      license='MIT',
      packages = find_packages('src'),
      package_dir = { '': 'src' },
      scripts = ['twine'],
      maintainer = 'Joshua Curl',
      maintainer_email = 'curljosh@msu.edu',
      url = 'https://github.com/joshuacurl/twine',
      long_description = open("README.md").read(),
      classifiers = ['Development Status :: 4 - Beta',
                     'Environment :: Console',
                     'Intended Audience :: Developers',
                     'Intended Audience :: System Administrators',
                     'License :: OSI Approved :: MIT License',
                     'Natural Language :: English',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python',
                     'Programming Language :: Other Scripting Engines',
                     'Topic :: Internet :: WWW/HTTP',
                     'Topic :: Software Development :: Testing',
                     ],
      test_suite = 'nose.collector'
      )
