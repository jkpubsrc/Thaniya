#!/usr/bin/python3


import typing
import os
import sys
import time

import jk_json
import jk_sysinfo
import jk_utils

from jk_appmonitoring import *

from thaniya_server.utils import SVGDiskSpaceGraphGenerator






fsCol = RFileSystemCollection()
fsCol.registerFileSystem(RFileSystem("Main", "/", bWeakDirRefs=False))

fsCol.registerDirectory(RDirectory("Downloads", os.path.join(jk_utils.users.getUserHome(), "Downloads"), 30))
fsCol.registerDirectory(RDirectory("DevPriv", os.path.join(jk_utils.users.getUserHome(), "DevPriv"), 30))
fsCol.registerDirectory(RDirectory("bin", os.path.join(jk_utils.users.getUserHome(), "bin"), 30))
fsCol.registerDirectory(RDirectory("NLPTools", os.path.join(jk_utils.users.getUserHome(), "NLPTools"), 30))

print("Getting disk space data ...")
fsCol.update()
print("Done.")



gen = SVGDiskSpaceGraphGenerator(fsCol.filesystems[0])

with open(os.path.basename(__file__) + ".svg", "w") as f:
	f.write(gen.toSVG(800))





















