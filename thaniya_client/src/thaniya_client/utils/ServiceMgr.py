#
# For this module to work you require either to invoke this as root or add the following line to your sudoers file (assuming you
# invoke the script being "myuser"):
#
# <code>
# myuser         ALL=(root) NOPASSWD: /usr/sbin/service
# </code>
#


import os
import typing
import subprocess



from .ServiceInfo import ServiceInfo







class ServiceMgr:

	@staticmethod
	def __tryExtract(line:str, keyword:str):
		keyword += ":"

		line = line.strip()
		if line.startswith(keyword):
			return line[len(keyword):].strip()

		return None
	#

	@staticmethod
	def getStatus(serviceName:str):
		cmd = [
			"/usr/sbin/service",
			serviceName,
			"status"
		]

		p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		(stdout, stderr) = p.communicate(timeout=20)
		#if p.returncode != 0:
		#	raise Exception("Failed!")

		stdOutDataLines = stdout.decode("utf-8").split("\n")
		stdErrDataLines = stderr.decode("utf-8").split("\n")

		#for line in stdOutDataLines:
		#	print(repr(line))

		# ----

		assert stdOutDataLines[0].startswith("● ")
		pos = stdOutDataLines[0].find(" - ")
		if pos <= 0:
			description = stdOutDataLines[0][pos + 2:].strip()
		else:
			description = None

		active = None
		pid = None
		isRunning = None

		for line in stdOutDataLines[1:]:
			r = ServiceMgr.__tryExtract(line, "Active")
			if r:
				active = r
				isRunning = active.find("(running)") >= 0
			r = ServiceMgr.__tryExtract(line, "Main PID")
			if r:
				pid = r

		#print("description:", description)
		#print("active:", active)
		#print("isRunning:", isRunning)
		#print("pid:", pid)

		return ServiceInfo(serviceName, description, active, isRunning, pid)
	#

	@staticmethod
	def start(serviceName:str):
		assert isinstance(serviceName, str)

		cmd = []

		if os.geteuid() != 0:
			cmd.append("/usr/bin/sudo")

		cmd.extend([
			"/usr/sbin/service",
			serviceName,
			"start"
		])

		p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		(stdout, stderr) = p.communicate(timeout=20)

		if p.returncode == 0:
			return

		"""
		print(p.returncode)
		stdOutDataLines = stdout.decode("utf-8").split("\n")
		stdErrDataLines = stderr.decode("utf-8").split("\n")

		for line in stdOutDataLines:
			print(repr(line))
		for line in stdErrDataLines:
			print(repr(line))
		"""

		raise Exception("Failed to stop service: " + serviceName)
	#

	@staticmethod
	def stop(serviceName:str):
		assert isinstance(serviceName, str)

		cmd = []

		if os.geteuid() != 0:
			cmd.append("/usr/bin/sudo")

		cmd.extend([
			"/usr/sbin/service",
			serviceName,
			"stop"
		])

		p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		(stdout, stderr) = p.communicate(timeout=20)

		if p.returncode == 0:
			return

		"""
		print(p.returncode)
		stdOutDataLines = stdout.decode("utf-8").split("\n")
		stdErrDataLines = stderr.decode("utf-8").split("\n")

		for line in stdOutDataLines:
			print(repr(line))
		for line in stdErrDataLines:
			print(repr(line))
		"""

		raise Exception("Failed to stop service: " + serviceName)
	#

#


























