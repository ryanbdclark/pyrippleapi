from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="pyrippleapi",
    version="2023.7.1",
    description="Ripple energy api wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ryanbdclark/pyrippleapi",
    author="Ryan Clark",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="ripple, api, energy",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=["aiohttp"],
)
