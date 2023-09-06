from setuptools import find_packages, setup
from _version import __version__

setup(
    name='sweb',
    version=__version__,
    author = "Irving Martinez",
    packages=find_packages(),
    install_requires =[
        'beautifulsoup4==4.12.2',
        'certifi==2023.7.22',
        'charset-normalizer==3.2.0',
        'idna==3.4',
        'lxml==4.9.3',
        'requests==2.31.0',
        'soupsieve==2.5',
        'urllib3==2.0.4',
    ],
    entry_points = {
        'console_scripts': [
            'sweb = src.__main__:main',
        ]
    }
)