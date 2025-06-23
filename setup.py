# setup.py
from setuptools import setup, find_packages

setup(
    name="AWG_Automation",
    version="0.1.0",
    author="Vijayanand Kv",
    description="Python SCPI interface for controlling Keysight M8195A AWG",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pyvisa",
        "numpy",
        "matplotlib",
        # add any other dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
