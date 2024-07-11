from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in api_integration/__init__.py
from api_integration import __version__ as version

setup(
	name="api_integration",
	version=version,
	description="DAS",
	author="DAS",
	author_email="digitalasiasolusindo@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
