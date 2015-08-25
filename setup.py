#!/usr/bin/env python
from setuptools import setup


setup(name='omc',
      version='0.0.0',
      description='OhMyCron, bringing your environments together.',
      packages=['omc'],
      entry_points={'console_scripts': ['omc = omc.__main__:main']},
      install_requires=['argh'],
      setup_requires=['setuptools'],
      tests_require=['flake8'],
      classifiers=['Environment :: Console',
                   'Intended Audience :: Developers',
                   'Operating System :: Unix',
                   'Programming Language :: Python',
                   'License :: OSI Approved :: ISC License (ISCL)',
                   'Topic :: System',
                   'Topic :: Software Development',
                   'Development Status :: 4 - Beta'])
