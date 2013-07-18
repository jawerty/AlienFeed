#!/usr/bin/env python

from setuptools import setup

setup(name='AlienFeed',
      version='0.2.7',
      description='AlienFeed is a simple Reddit client for viewing and opening links from your console.',
      author='Jared Wright',
      license='MIT',
      keywords = "AlienFeed alien reddit feed rss tool cli",
      author_email='jawerty210@gmail.com',
      url='http://github.com/jawerty/AlienFeed',
      scripts=['alienfeed/alien.py'],
      install_requires=['praw'],
      entry_points = {
        'console_scripts': [
            'alienfeed = alien:main'
        ],
	  }
     )