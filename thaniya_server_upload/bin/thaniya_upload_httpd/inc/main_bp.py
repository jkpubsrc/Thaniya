
import random
import flask
import flask_login

import jk_logging
import jk_typing

#from thaniya_server import AppRuntime
from thaniya_server_upload import AppRuntimeUploadHttpd
from thaniya_server.utils import SVGDiskSpaceGraphGenerator








@jk_typing.checkFunctionSignature()
def init_blueprint(app:flask.Flask, appRuntime:AppRuntimeUploadHttpd, log:jk_logging.AbstractLogger):
	assert isinstance(appRuntime, AppRuntimeUploadHttpd)

	main_bp = flask.Blueprint("main", __name__)

	# --------------------------------------------------------------------------------------------------------------------------------

	@main_bp.route("/index.html")
	#@flask_login.login_required
	def index():
		if flask_login.current_user.is_anonymous:
			return flask.render_template(
				"anonymous/index.jinja2",
				rndid = random.randint(0, 999999),
				htmlHeadTitle = "Thaniya Upload - /",
				)

		else:
			return flask.render_template(
				"authenticated/index.jinja2",
				rndid = random.randint(0, 999999),
				user = flask_login.current_user,
				htmlHeadTitle = "Thaniya Upload - /",
				visNavPath = "/ Index",
				)
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	#@main_bp.route("/testpages/index.jinja2")
	#def testpages_index():
	#	return flask.render_template("testpages/index.html", rndid=random.randint(0, 999999))
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	@main_bp.route("/overview")
	@flask_login.login_required
	def overview():
		fsInfoList = []
		for fs in appRuntime.fileSystemCollection.filesystems:
			fs.update()
			gen = SVGDiskSpaceGraphGenerator(fs)
			fsInfoList.append(gen)

		return flask.render_template(
			"authenticated/overview.jinja2",
			rndid = random.randint(0, 999999),
			user = flask_login.current_user,
			htmlHeadTitle = "Thaniya Upload - /overview",
			visNavPath = "/ Overview",
			fsInfoList = fsInfoList,							# RFileSystem[]
			slotList = appRuntime.uploadSlotMgr.slots			# UploadSlot[]
			)
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	@main_bp.route("/profile")
	@flask_login.login_required
	def profile():
		return flask.render_template(
			"authenticated/profile.jinja2",
			rndid = random.randint(0, 999999),
			)
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	app.register_blueprint(main_bp)

#















