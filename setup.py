from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='Publish',
    version='1.2.0',
    author='Alfred Dominic, Shahul Hameed',
    author_email='alfie.2012@gmail.com',
    packages=find_packages(exclude=[]),
    scripts=['publish.py','README.md'],
    url='https://github.com/alfie-max/publish',
    description='Program to broadcast an announcement on multiple social media channels',
    long_description=open('README.md').read(),
    install_requires=[
        "Pillow==2.5.3",
        "argparse==1.2.1",
        "configobj==5.0.5",
        "py==1.4.23",
        "six==1.7.3",
        "tweepy==2.3.0",
        "wsgiref==0.1.2",
    ],
)
