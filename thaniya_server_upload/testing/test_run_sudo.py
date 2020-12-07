#!/usr/bin/python3




import os

import thaniya_server.sysusers





s = thaniya_server.sysusers.SudoScriptRunner("/etc/thaniya/sudoscripts")

print()

print(s.scriptNames)

print()

r = s.run1("script_test", "12")
r.dump()

print()

r = s.run1("script_test2", "12", stdin="foo-bar")
r.dump()

print()





