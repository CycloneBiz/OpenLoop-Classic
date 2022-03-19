from flask import Blueprint, jsonify, render_template, redirect, url_for, request
from openloop.gui import NavElement, Version, System
from openloop.chart import translate as chart_translate
from werkzeug.security import generate_password_hash
from werkzeug import secure_filename
import os

class Web_Handler:
    web = Blueprint("web", __name__, "static", "templates")

    def __init__(self, db, workers, auth, alerts, crossflow) -> None:
        self.db = db
        self.alerts = alerts
        self.auth = auth

        def get_navs(hidden=False):
            if not hidden:
                navs = {"OPENLOOP INTERNAL": []}
                for i in workers.plugin_inst:
                    selection = i.settings.get("category", "PLUGINS")

                    if i.settings.get("hidden", False) == False:
                        if not selection in navs:
                            navs[selection] = []

                        navs[selection].append(NavElement(i.settings.get("iconame", i.name), f"/plugins/{i.name}"))
            else:
                navs = {"PLUGINS HIDDEN": []}

            return navs

        self.get_navs = get_navs
        
        @self.web.route("/")
        @auth.login_required
        def index():
            store_settings = db["properties"]["storage"]
            return render_template(
                "index.html",
                navbar=get_navs(),
                drivers=len(workers.plugin_inst),
                dash=crossflow.dash.dash_buttons,
                storage_used=f"{db.size/store_settings['divide']}{store_settings['unit']}",
                alerts=alerts
            )

        @self.web.route("/trylogin/here")
        @auth.login_required
        def try_login():
            return redirect(url_for(".index"))

        @self.web.route("/start", methods=["GET", "POST"])
        def startup():
            if db["properties"]["startup"] == True:
                return redirect(url_for(".index"))
            else:
                if request.method == "GET" or request.form.get("password", None)==None:
                    return render_template("starting.html")
                elif request.form.get("password", None) == "":
                    return render_template("starting.html", notice="Your password cannot be nothing!")
                else:
                    passw = generate_password_hash(request.form["password"])
                    db["properties"]["users"]["admin"] = passw
                    db["properties"]["startup"] = True
                    return redirect(url_for(".try_login"))

        @self.web.route("/about")
        @auth.login_required
        def settings_view():
            return render_template("settings.html", navbar=get_navs(), version=Version(), system=System(), alerts=alerts)

        @self.web.route("/plugins/upload")
        @auth.login_required
        def fix_upload_issue():
            # Fixes browser issue whenever theres a space in a route
            return redirect(url_for(".upload_plugin"))

        @self.web.route("/plugins/<driver>")
        @auth.login_required
        def show_driver_info(driver):
            found = False
            for i in workers.plugin_inst:
                if i.name == driver:
                    found = i
            if found != False:
                return render_template("sensor.html", navbar=get_navs(), settings=found.settings, name=found.name, chart=chart_translate(found.extract_features()), alerts=alerts, crossweb=found.crossweb, objected=found)
            else:
                return render_template("404.html", navbar=get_navs(), alerts=alerts, code=404, text="The plugin you requested does not exist"), 404

        @self.web.route("/plugins/<driver>/delete")
        @auth.login_required
        def delete_driver(driver):
            found = False
            for i in workers.plugin_inst:
                if i.name == driver:
                    found = i
            if found != False and found.name not in ["OpenLoop Saver", "OpenLoop Error"]:
                path = "plugins/"+found.path
                if os.path.exists(path):
                    os.remove(path)
                    return redirect(url_for(".list_plugin"))
                else:
                    return render_template("404.html", navbar=get_navs(), alerts=alerts, code=404, text="Looks like that plugin has already been removed, restart to see changes"), 404
            else:
                return render_template("404.html", navbar=get_navs(), alerts=alerts, code=404), 404

        @self.web.route("/plugins")
        @auth.login_required
        def list_plugin():
            return render_template("plugins.html", navbar=get_navs(), alerts=alerts, plugins=workers.plugin_inst)

        @self.web.route("/upload", methods=["GET", "POST"])
        @auth.login_required
        def upload_plugin():
            if request.method == "GET":
                return render_template("upload.html", navbar=get_navs(), alerts=alerts)
            else:
                req = request.files["file"]
                if req.filename.endswith(".pyl"):
                    req.save("plugins/"+secure_filename(req.filename))
                    return redirect(url_for(".upload_plugin"))
                else:
                    return "Only can import .pyl files (Python Logic Script)"
    
    def assign_errors(self, app):
        @app.errorhandler(404)
        @self.auth.login_required
        def not_found(e):
            return render_template("404.html", alerts=self.alerts, code=404, text="Um... That dosent exist"), 404

        @app.errorhandler(500)
        @self.auth.login_required
        def not_found(e):
            return render_template("404.html", alerts=[], code=500, text="Looks like you venturd too far!", navbar=self.get_navs(True)), 500

        def not_found():
            return render_template("404.html", alerts=[], code=401, text="Bad Guy or Sad User?", start=True, navbar=self.get_navs(True)), 401

        self.auth.error_handler(not_found)