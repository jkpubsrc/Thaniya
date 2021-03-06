################################################################################
################################################################################
###
###  This file is automatically generated. Do not change this file! Changes
###  will get overwritten! Change the source file for "setup.py" instead.
###  This is either 'packageinfo.json' or 'packageinfo.jsonc'
###
################################################################################
################################################################################


from setuptools import setup

def readme():
	with open("README.md", "r", encoding="UTF-8-sig") as f:
		return f.read()

setup(
	author = "Jürgen Knauth",
	author_email = "pubsrc@binary-overflow.de",
	classifiers = [
		"Development Status :: 3 - Alpha",
		"License :: OSI Approved :: Apache Software License",
		"Programming Language :: Python :: 3",
	],
	description = "The Thaniya backup server.",
	include_package_data = False,
	install_requires = [
		"flask",
		"flask_login",
		"thaniya_common",
		"Babel",
	],
	keywords = [
		"thaniya",
	],
	license = "Apache2",
	name = "thaniya_server",
	packages = [
		"thaniya_server",
		"thaniya_server.session",
		"thaniya_server.app",
		"thaniya_server.api",
		"thaniya_server.usermgr",
		"thaniya_server.utils",
		"thaniya_server.sysusers",
		"thaniya_server.flask",
		"thaniya_server.jobs",
	],
	version = "0.2021.2.15",
	zip_safe = False,
	long_description = readme(),
	long_description_content_type="text/markdown",
)
