
import random
import flask
import flask_login

import jk_logging

from thaniya_server_archive import AppRuntimeArchiveHttpd







def init_blueprint(app:flask.Flask, appRuntime:AppRuntimeArchiveHttpd, log:jk_logging.AbstractLogger):
	assert isinstance(appRuntime, AppRuntimeArchiveHttpd)

	main_bp = flask.Blueprint("testpages", __name__)

	# --------------------------------------------------------------------------------------------------------------------------------

	@main_bp.route("/testpages/index.html")
	def testpages_index():
		return flask.render_template("testpages/index.html", rndid=random.randint(0, 999999))
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	@main_bp.route("/testpages/index-form.html")
	def testpages_index_form():
		return flask.render_template("testpages/index-form.html", rndid=random.randint(0, 999999))
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	@main_bp.route("/testpages/index-hugecentertitle.html")
	def testpages_index_hugecentertitle():
		return flask.render_template("testpages/index-hugecentertitle.html", rndid=random.randint(0, 999999))
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	@main_bp.route("/testpages/index-article.html")
	def testpages_index_article():
		return flask.render_template("testpages/index-article.html", rndid=random.randint(0, 999999))
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	app.register_blueprint(main_bp)

#















