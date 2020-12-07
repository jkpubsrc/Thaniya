#!/usr/bin/python3




from thaniya_server_archive import *








pattern = FileNamePattern("*.json")
assert pattern.match("foo.json")
assert pattern.match(".json")
assert not pattern.match("foo.jsonc")











