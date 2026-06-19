from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='seeker-improved',
    version='2.0.0',
    description='Red team geolocation and device fingerprint capture tool',
    python_requires='>=3.7',
    install_requires=[
        'requests>=2.20.0',
        'psutil>=5.0.0',
        'packaging>=21.0',
    ],
    packages=find_packages(),
    package_data={
        '': [
            'template/**/*',
            'js/*',
            'metadata.json',
            'template/sample.kml',
        ],
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'seeker=seeker:main',
        ],
    },
)
