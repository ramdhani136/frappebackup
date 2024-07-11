from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in overdue_app/__init__.py
from overdue_app import __version__ as version

setup(
	name="overdue_app",
	version=version,
	description="Overdue App",
	author="DAS",
	author_email="digitalasiasolusindo@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
