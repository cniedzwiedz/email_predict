__author__ = 'cniedzwiedz'

from setuptools import setup

setup(name='email_predict',
      version='0.1.0',
      description='',
      author='Chris Niedzwiedz',
      author_email='cniedzwiedz@gmail.com',
      license='Proprietary',
      packages=['email_predict'],
      install_requires=['beautifulsoup4',
                        'python-dateutil',
                        'ofxparse'
                        ],
      scripts=['bin/azn_reconcile.py'],
      zip_safe=False)
