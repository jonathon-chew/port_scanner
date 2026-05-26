
from setuptools import find_packages
from setuptools import setup


setup(
    name="port_scanner",
    version="0.0.1",
    description="A way to scan ports on any device",
    author="Jonathon Chew",
    author_email="noreply@example.com",
    url="",
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=("tests*",)),
    entry_points={
        "console_scripts": [
            "port-scanner=port_scanner.__main__:main",
        ]
    },
)
