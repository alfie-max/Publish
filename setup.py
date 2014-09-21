from setuptools import setup, find_packages

setup(
    name = 'python-publish',
    version = '1.0.0',
    author = 'Alfred Dominic, Shahul Hameed',
    author_email = 'alfie.2012@gmail.com',
    packages = find_packages(exclude=[]),
    scripts = ['publish'],
    url = 'https://github.com/alfie-max/publish',
    description = 'Program to broadcast an announcement on multiple social media channels',
    long_description = open('README.md').read(),
    install_requires=[
        "argparse==1.2.1",
        "beautifulsoup4==4.3.2",
        "configobj==5.0.5",
        "facebook-sdk==0.4.0",
        "mechanize==0.2.5",
        "Pillow==2.5.3",
        "termcolor==1.1.0",
        "tweepy==2.3.0",
        "wsgiref==0.1.2",
    ],
)
