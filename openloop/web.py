from flask import Blueprint, jsonify, render_template
from matplotlib import category
from openloop.gui import NavElement, Version, System
from openloop.chart import translate as chart_translate

class Web_Handler:
    web = Blueprint("web", __name__, "static", "templates")

    def __init__(self, db, workers, auth, alerts) -> None:
        self.db = db

        def get_navs():
            navs = {"OPENLOOP INTERNAL": []}

            for i in workers.plugin_inst:
                selection = i.settings.get("category", "PLUGINS")

                if not selection in navs:
                    navs[selection] = []

                navs[selection].append(NavElement(i.settings.get("iconame", i.name), f"/plugins/{i.name}"))


            return navs
        
        @self.web.route("/")
        @auth.login_required
        def index():
            store_settings = db["properties"]["storage"]

            return render_template(
                "index.html",
                navbar=get_navs(),
                drivers=len(workers.plugin_inst),
                energy="NaN",
                storage_used=f"{db.size/store_settings['divide']}{store_settings['unit']}",
                alerts=alerts
            )

        @self.web.route("/about")
        @auth.login_required
        def settings_view():
            return render_template("settings.html", navbar=get_navs(), version=Version(), system=System(), alerts=alerts)

        @self.web.route("/plugins/<driver>")
        @auth.login_required
        def show_driver_info(driver):
            found = False
            for i in workers.plugin_inst:
                if i.name == driver:
                    found = i
            if found != False:
                return render_template("sensor.html", navbar=get_navs(), settings=found.settings, name=found.name, chart=chart_translate(found.extract_features()), alerts=alerts, crossweb=found.crossweb)
            else:
                return render_template("404.html", navbar=get_navs(), alerts=alerts), 404

        @self.web.route("/plugins")
        def list_plugin():
            return render_template("plugins.html", navbar=get_navs(), alerts=alerts, plugins=workers.plugin_inst)