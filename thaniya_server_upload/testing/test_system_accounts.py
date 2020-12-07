#!/usr/bin/python3




import os

import thaniya_server.sysusers





s = thaniya_server.sysusers.SudoScriptRunner("/etc/thaniya/sudoscripts")
am = thaniya_server.sysusers.SystemAccountManager(s)

print()

for account in am.accounts:
	account.dump()

print()

for account in am.accounts:
	print("Disabling: " + account.userName)
	account.disable()

print()

print("Updating ...")
am.update()

print()

for account in am.accounts:
	account.dump()

print()

for account in am.accounts:
	print("Enabling: " + account.userName)
	account.enable()

print()

print("Updating ...")
am.update()

print()

for account in am.accounts:
	account.dump()

print()





