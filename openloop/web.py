from flask import Blueprint, jsonify, render_template
from openloop.gui import NavElement, Version, System
from openloop.chart import translate as chart_translate

class Web_Handler:
    web = Blueprint("web", __name__, "static", "templates")

    def __init__(self, db, workers, auth, alerts) -> None:
        self.db = db

        def get_navs(highlight):
            navs = []

            navs.append(NavElement("Dashboard", "/", "fas fa-tachometer-alt", False))

            for i in workers.plugin_inst:
                navs.append(NavElement(i.name, f"/driver/{i.name}", i.settings["icon"], False))

            navs.append(NavElement("Settings", "/settings", "fa fa-gear", False))

            for i in navs:
                if i.name == highlight:
                    i.active = "active"

            return navs
        
        @self.web.route("/")
        @auth.login_required
        def index():
            store_settings = db["properties"]["storage"]

            return render_template(
                "index.html",
                navbar=get_navs("Dashboard"),
                drivers=len(workers.plugin_inst),
                energy="NaN",
                storage_used=f"{db.size/store_settings['divide']}{store_settings['unit']}",
                alerts=alerts
            )

        @self.web.route("/settings")
        @auth.login_required
        def settings_view():
            return render_template("settings.html", navbar=get_navs("Settings"), version=Version(), system=System(), alerts=alerts)

        @self.web.route("/driver/<driver>")
        @auth.login_required
        def show_driver_info(driver):
            found = False
            for i in workers.plugin_inst:
                if i.name == driver:
                    found = i
            if found != False:
                return render_template("sensor.html", navbar=get_navs(driver), settings=found.settings, name=found.name, chart=chart_translate(found.extract_features()), alerts=alerts)
            else:
                return render_template("404.html", navbar=get_navs(""), alerts=alerts), 404
