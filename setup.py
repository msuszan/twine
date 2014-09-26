#!/usr/bin/env python

from setuptools import setup

# setup information
setup(name = 'twine',
      description = 'An implementation of twill based on spynner',
      author = 'Joshua Curl, C. Titus Brown, and Ben R. Taylor',
      author_email = 'curljosh@msu.edu',

      license='MIT',
      packages = ['twine', 'twine.extensions',
                  'twine.extensions.match_parse'],
      # allow both 
      entry_points = dict(console_scripts=['twine = twine.shell:main'],),
      scripts = ['twill-fork'],

      maintainer = 'Joshua Curl',
      maintainer_email = 'curljosh@msu.edu',
      url = 'https://github.com/joshuacurl/twine',
      long_description = """\
twill is an implementation of the twill scripting language using spynner. This will allow for some new features, most notably JavaScript support.
""",
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
