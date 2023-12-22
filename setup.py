import sys
from setuptools import setup, find_packages

setup(name="tfvis",
    version="0.0.1",
    description="Simple Python API to Meshcat for grokking transforms",
    url="https://github.com/rdeits/meshcat-python",
    author="Raghava Uppuluri",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
      "meshcat >= 0.3.2",
      "numpy",
    ],
    extras_require={
      'examples': ['gtsam',
                   'argparse'],
    },
    zip_safe=False,
)
