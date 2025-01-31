from setuptools import setup, find_packages

setup(
    name="kcolorconverter",
    version="0.0.2",
    packages=find_packages(),
    description=(
        "A utility library for converting colors between formats like RGB, RGBA, "
        "HEX6, and HEX8. Provides flexible handling of color representations for "
        "Python applications."
    ),
    author="kokaito",
    author_email="kokaito.git@gmail.com",
    url="https://github.com/kokaito-git/kcolorconverter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
    ],
    install_requires=[
        "typing-extensions",
    ]
)
