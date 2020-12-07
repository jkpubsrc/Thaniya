#!/usr/bin/python3



import sys
import typing
import os
import random
import mimetypes
import datetime
import signal

import flask

import jk_typing
import jk_logging

import thaniya_common
import thaniya_server
import thaniya_server_upload
import thaniya_server.flask








DEBUG = True
#USE_PRODUCTION_WEBSERVER = True
USE_PRODUCTION_WEBSERVER = False







################################################################################################################################

mimetypes.init()

APP_BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = flask.Flask(
	__name__,
	static_folder=APP_BASE_DIR + "/static",
	template_folder=APP_BASE_DIR + "/templates",
	)

app.secret_key = os.urandom(32)					# good secret key; as a new one is generated each time sessions should invalidate automatically on server restart;

app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=31)
#app.config["PREFERRED_URL_SCHEME"] = "https"
#app.config["SESSION_COOKIE_SECURE"] = True					# if this is set to True cookies will only be stored it https is used!
if DEBUG:
	app.config["TEMPLATES_AUTO_RELOAD"] = True
	app.config["EXPLAIN_TEMPLATE_LOADING"] = True
	app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

randInt = random.randint(0, 999999)

for filterClass in thaniya_server.flask.ALL_FLASK_FILTER_CLASSES:
	filterInst = filterClass()
	app.add_template_filter(filterInst.__call__, filterInst.name)

#@app.context_processor
#def inject_randInt() -> dict:
#	return dict(randInt=randInt)
##

################################################################################################################################

# initialize main application object

with jk_logging.wrapMain() as log:
	appRuntime = thaniya_server_upload.AppRuntimeUploadHttpd(__file__, log)
	os.chdir(appRuntime.appBaseDirPath)

	# register blueprints

	from inc.auth_bp import init_blueprint as _init_auth_blueprint
	_init_auth_blueprint(app, appRuntime, log)

	from inc.main_bp import init_blueprint as _init_main_blueprint
	_init_main_blueprint(app, appRuntime, log)

	from inc.api_bp import init_blueprint as _init_api_blueprint
	_init_api_blueprint(app, appRuntime, log)

	from inc.testpages_bp import init_blueprint as _init_testpages_blueprint
	_init_testpages_blueprint(app, appRuntime, log)

################################################################################################################################











################################################################################################################################
## Main Index Page
################################################################################################################################

@app.route("/")
def index0():
	return flask.redirect("/index.html")
#

################################################################################################################################
################################################################################################################################
################################################################################################################################



if DEBUG:
	print("Initialization complete, now starting webserver ...")

signal.signal(signal.SIGUSR1, appRuntime.onSIGUSR1)

if USE_PRODUCTION_WEBSERVER:
	from waitress import serve
	serve(app, host=appRuntime.cfg.httpd["interface"], port=appRuntime.cfg.httpd["port"], threads=8)
else:
	app.run(host=appRuntime.cfg.httpd["interface"], port=appRuntime.cfg.httpd["port"])











