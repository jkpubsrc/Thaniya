#!/usr/bin/python3




import os

import jk_json

from thaniya_server.utils import *



pf = ProcessFilter(cmd="/usr/bin/python3", argsMatcher=lambda x: (x == "test_receive_signals.py") or (x.endswith("/test_receive_signals.py")))
#for jDict in pf.findProcessStructs():
#	print(jDict)

p = ProcessNotifier(pf)
n = p.notifySIGHUP()
print("{} processes notified.".format(n))






