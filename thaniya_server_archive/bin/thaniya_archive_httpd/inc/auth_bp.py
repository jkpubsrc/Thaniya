

import flask
import flask_login
import werkzeug.security

import jk_logging

#from thaniya_server import IAppRuntimeUserMgrx
import thaniya_server.usermgr






def init_blueprint(app:flask.Flask, appRuntime, log:jk_logging.AbstractLogger):
	#assert isinstance(appRuntime, IAppRuntimeUserMgr)

	login_manager = flask_login.LoginManager()
	login_manager.login_view = "auth.login"
	login_manager.init_app(app)
	login_manager.session_protection = "strong"

	auth_bp = flask.Blueprint("auth", __name__)

	@login_manager.user_loader
	def load_user(user_id:str) -> thaniya_server.usermgr.BackupUser:
		print(">> load_user(" + repr(user_id) + ")")
		return appRuntime.userMgr.getUser(user_id)
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	@auth_bp.route("/login")
	def login():
		print("current_user =", flask_login.current_user)
		if flask_login.current_user.is_anonymous:
			return flask.render_template("anonymous/login.jinja2")
		else:
			return flask.redirect("/index.html")
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	"""
	@auth_bp.route("/signup")
	def signup():
		print("current_user =", flask_login.current_user)
		return "Signup"
	#
	"""

	# --------------------------------------------------------------------------------------------------------------------------------

	@auth_bp.route("/logout")
	@flask_login.login_required
	def logout():
		print("current_user =", flask_login.current_user)
		flask_login.logout_user()
		return flask.render_template("authenticated/logout.jinja2")
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	@auth_bp.route("/do_login", methods=["POST"])
	def do_login_post():
		#print("current_user =", flask_login.current_user)
		# login code goes here
		userName = flask.request.form.get("userName")
		password = flask.request.form.get("password")
		remember = True if flask.request.form.get("remember") else False

		user = appRuntime.userMgr.getUser(userName)

		# check if the user actually exists
		if user is None:
			#print("-- No such user: " + userName)
			flask.flash("Please check your login details and try again.", "error")
			return flask.redirect(flask.url_for("auth.login"))

		# take the user-supplied password, hash it, and compare it to the hashed password in the database
		#print("@@1", user.passwordHash)
		#print("@@2", password)
		if not werkzeug.security.check_password_hash(user.passwordHash, password):
			#print("-- Invalid password for user: " + userName)
			flask.flash("Please check your login details and try again.", "error")
			return flask.redirect(flask.url_for("auth.login")) # if the user doesn"t exist or password is wrong, reload the page

		# if the above check passes, then we know the user has the right credentials
		#print("-- User check: okay. Allowing login.")
		#print("@@3", flask_login.current_user)
		flask_login.login_user(user, remember=remember)
		#print("@@4", flask_login.current_user)

		nextURL = flask.request.args.get("next")
		if nextURL:
			if not flask.is_safe_url(nextURL):
				return flask.abort(400)
			if nextURL:
				#print("-- Redirecting to: " + nextURL)
				flask.redirect(nextURL)
			else:
				#print("-- Redirecting to: main.index.")
				return flask.redirect(flask.url_for("main.index"))
		else:
			#print("-- Redirecting to: main.index.")
			return flask.redirect(flask.url_for("main.index"))
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	app.register_blueprint(auth_bp)

#














