#!/usr/bin/env python3

import setuptools
import x9k3

with open("README.md", "r") as fh:
    readme = fh.read()

setuptools.setup(
    name="x9k3",
    version=x9k3.version(),
    author="Adrian of Doom and two really smart chicks in gogo boots",
    author_email="spam@iodisco.com",
    description="An HLS Segmenter with SCTE-35 Parsing and Injection",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/superkabuki/x9k3",
    packages=setuptools.find_packages(),
    scripts=["bin/x9k3"],
    platforms="all",
    install_requires=[
        "threefive >= 3.0.55",
        "m3ufu >= 0.0.93",
    ],
    classifiers=[
        "License :: OSI Approved :: Sleepycat License",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Operating System :: POSIX :: BSD :: OpenBSD",
        "Operating System :: POSIX :: BSD :: NetBSD",
        "Operating System :: POSIX :: Linux",
        "Topic :: Multimedia :: Video",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    python_requires=">=3.9",
)
