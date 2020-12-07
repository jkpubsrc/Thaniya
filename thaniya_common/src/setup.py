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
	description = "Common classes for Thaniya implementations, client and server.",
	include_package_data = False,
	install_requires = [
		"flask",
		"flask_login",
		"jk_argparsing",
		"jk_console",
		"jk_exceptionhelper",
		"jk_json",
		"jk_logging",
		"jk_prettyprintobj",
		"jk_pwdinput",
		"jk_simpleobjpersistency",
		"jk_svg",
		"jk_typing",
		"jk_utils",
	],
	keywords = [
		"thaniya",
	],
	license = "Apache2",
	name = "thaniya_common",
	packages = [
		"thaniya_common",
		"thaniya_common.cfg",
		"thaniya_common.utils",
	],
	version = "0.2021.1.18",
	zip_safe = False,
	long_description = readme(),
	long_description_content_type="text/markdown",
)
