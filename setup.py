import os
from datetime import datetime
from setuptools import setup, find_packages

version = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

install_requires = [
    'tornado==2.4']

setup(name='msarullo.tornadoapp',
    version=version,
    description="Test web application",
    long_description="Web application used to test scaling and web sockets with Amazon, RightScale, and caching technologies.",
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='',
    author='Mike Sarullo',
    author_email='',
    url='',
    license='',
    packages=find_packages('src'),
    package_dir={
        '': 'src'},
    namespace_packages=['msarullo'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'main = msarullo.entrypoint:main']})
