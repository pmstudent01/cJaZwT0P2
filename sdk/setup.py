"""
Setup script for the Vehicle Service Python SDK.
"""

from setuptools import setup, find_packages

setup(
    name="vehicle-service-sdk",
    version="1.0.0",
    description="Python SDK for the Vehicle Service API, generated from the Vehicle Service Collection",
    packages=find_packages(),
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
