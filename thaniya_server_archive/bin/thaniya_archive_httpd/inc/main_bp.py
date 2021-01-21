
import random
import datetime
import flask
import flask_login
import werkzeug.security

import jk_logging

from thaniya_server_archive import AppRuntimeArchiveHttpd
from thaniya_server.utils import SVGDiskSpaceGraphGenerator
from thaniya_common.utils import APIPassword









def init_blueprint(app:flask.Flask, appRuntime:AppRuntimeArchiveHttpd, log:jk_logging.AbstractLogger):
	assert isinstance(appRuntime, AppRuntimeArchiveHttpd)

	main_bp = flask.Blueprint("main", __name__)

	# --------------------------------------------------------------------------------------------------------------------------------

	@main_bp.route("/index.html")
	#@flask_login.login_required
	def index():
		if flask_login.current_user.is_anonymous:
			return flask.render_template(
				"anonymous/index.jinja2",
				rndid = random.randint(0, 999999),
				htmlHeadTitle = "Thaniya Archive - /",
				)

		else:
			return flask.render_template(
				"authenticated/index.jinja2",
				rndid = random.randint(0, 999999),
				user = flask_login.current_user,
				htmlHeadTitle = "Thaniya Archive - /",
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
			htmlHeadTitle = "Thaniya Archive - /overview",
			visNavPath = "/ Overview",
			fsInfoList = fsInfoList,
			volumeList = appRuntime.backupVolumeMgr.listVolumes(appRuntime.log),
			archiveList = appRuntime.archiveMgr.archives,
		)
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	@main_bp.route("/backups-own")
	@flask_login.login_required
	def backups_own():

		# group backups by date

		backupGroupList = []
		_lastDate = None
		_currentGroup = None
		for backup in appRuntime.backupMgr.getBackups(
				actingUser = flask_login.current_user,
			):

			if backup.lBackupStartDate != _lastDate:
				_currentGroup = []
				_lastDate = backup.lBackupStartDate
				backupGroupList.append((
					datetime.datetime(_lastDate[0], _lastDate[1], _lastDate[2], 0, 0, 0, 0),
					_currentGroup
				))
			_currentGroup.append(backup)

		# 'backupGroupList' now contains tuples consisting of datetime and Backup[]

		# ----

		return flask.render_template(
			"authenticated/backups_own.jinja2",
			rndid = random.randint(0, 999999),
			user = flask_login.current_user,
			htmlHeadTitle = "Thaniya Archive - /backups-own",
			visNavPath = "/ Own Backups",
			backupGroupList = backupGroupList,
		)
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	@main_bp.route("/profile")
	@flask_login.login_required
	def profile():
		return flask.render_template(
			"authenticated/profile.jinja2",
			rndid = random.randint(0, 999999),
			user = flask_login.current_user,
			htmlHeadTitle = "Thaniya Archive - /profile",
			visNavPath = "/ Profile",
		)
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	@main_bp.route("/profile_chpasswd_own")
	@flask_login.login_required
	def profile_chpasswd_own():
		return flask.render_template(
			"authenticated/profile_chpasswd_own.jinja2",
			rndid = random.randint(0, 999999),
			user = flask_login.current_user,
			htmlHeadTitle = "Thaniya Archive - /chpasspwd-own",
			visNavPath = "/ Change own login password",
		)
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	@main_bp.route("/profile_chuploadpasswd_own")
	@flask_login.login_required
	def profile_chuploadpasswd_own():
		return flask.render_template(
			"authenticated/profile_chuploadpasswd_own.jinja2",
			rndid = random.randint(0, 999999),
			user = flask_login.current_user,
			htmlHeadTitle = "Thaniya Archive - /chuploadpasspwd-own",
			visNavPath = "/ Change backup upload password",
			newBackupUploadPwd = APIPassword.generate(),
		)
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	@main_bp.route("/do_chpasswd_own", methods=["POST"])
	@flask_login.login_required
	def do_chpasswd_own_post():
		#print("current_user =", flask_login.current_user)

		# get data
		user = flask_login.current_user
		password_old = flask.request.form.get("password_old")
		password_new_1 = flask.request.form.get("password_new_1")
		password_new_2 = flask.request.form.get("password_new_2")

		# check if both new passwords match
		if password_new_1 != password_new_2:
			flask.flash("Please provide the same new password twice!", "error")
			return flask.redirect(flask.url_for("main.profile_chpasswd_own"))

		# check if new password is different
		if password_old == password_new_1:
			flask.flash("Please provide a new password!", "error")
			return flask.redirect(flask.url_for("main.profile_chpasswd_own"))

		# check if the new password is valid
		if len(password_new_1) >= 3:
			flask.flash("Please provide a new password of sufficient length!", "error")
			return flask.redirect(flask.url_for("main.profile_chpasswd_own"))

		# take the user-supplied password, hash it, and compare it to the hashed password in the database
		if not werkzeug.security.check_password_hash(user.passwordHash, password_old):
			flask.flash("Please provide your old password. The one you specified is not correct.", "error")
			return flask.redirect(flask.url_for("main.profile_chpasswd_own"))

		if not appRuntime.userMgr.hasPrivilege(user, "privChangeOwnLoginPwd"):
			flask.flash("Insufficient privileges.", "error")
			return flask.redirect(flask.url_for("main.profile_chpasswd_own"))

		# if the above check passes, then we know the user has the right credentials
		#print("-- User check: okay. Allowing password change.")
		user.passwordHash = werkzeug.security.generate_password_hash(password_new_1)
		try:
			user.store()
			flask.flash("Your password has been changed successfully.", "message")
		except Exception as ee:
			flask.flash("Failed to store the modifications to your user account.", "error")
		return flask.redirect(flask.url_for("main.profile"))
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	@main_bp.route("/do_chuploadpasswd_own", methods=["POST"])
	@flask_login.login_required
	def do_chuploadpasswd_own():
		#print("current_user =", flask_login.current_user)

		# get data
		user = flask_login.current_user
		login_password = flask.request.form.get("login_password")
		upload_password = flask.request.form.get("upload_password")

		# take the user-supplied password, hash it, and compare it to the hashed password in the database
		if not werkzeug.security.check_password_hash(user.passwordHash, login_password):
			flask.flash("Please provide your valid login password. The one you specified is not correct.", "error")
			return flask.redirect(flask.url_for("main.profile_chuploadpasswd_own"))

		if not appRuntime.userMgr.hasPrivilege(user, "privChangeOwnBackupUploadPwd"):
			flask.flash("Insufficient privileges.", "error")
			return flask.redirect(flask.url_for("main.profile_chuploadpasswd_own"))

		# if the above check passes, then we know the user has the right credentials
		#print("-- User check: okay. Allowing password change.")
		user.uploadPwd = APIPassword(upload_password)
		try:
			user.store()
			flask.flash("Your backup upload password has been changed successfully.", "message")
		except Exception as ee:
			flask.flash("Failed to store the modifications to your user account.", "error")
		return flask.redirect(flask.url_for("main.profile"))
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	app.register_blueprint(main_bp)

#















