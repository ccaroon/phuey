from setuptools import setup
import phuey.version

setup(
    name='phuey',
    version=phuey.version.VERSION,
    packages=['phuey'],
    package_dir={'phuey': 'phuey'},
    install_requires=[
        'rgbxy >= 0.5',
        'requests >= 2.26.0',
    ],
    entry_points={
        'console_scripts': [
            'phuey=phuey.main:cli',
        ],
    },
)
