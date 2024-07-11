from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in etm_qr_code/__init__.py
from etm_qr_code import __version__ as version

setup(
	name="etm_qr_code",
	version=version,
	description="An ETM apps for generate QR Code",
	author="DAS DEV",
	author_email="das@das.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
