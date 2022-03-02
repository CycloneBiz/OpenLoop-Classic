from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
import requests
import os

class API_Handler:
    api = Blueprint("api", __name__, "static", "templates")

    def __init__(self, db, workers, auth, alerts, crossflow) -> None:
        self.db = db

        @self.api.route("/")
        @auth.login_required
        def give_version():
            return {"version": 0.01}

        @self.api.route("/setpass")
        @auth.login_required
        def set_password():
            if request.headers.get("password", False)==False:
                return {"completed": False, "reason": "No Password Headers"}, 500
            else:
                password = request.headers.get("password")
                db["properties"]["users"]["admin"] = generate_password_hash(password)
                return {"completed": True}

        @self.api.route("/setpass/<user>")
        @auth.login_required
        def set_password_specific(user : str):
            if request.headers.get("password", False)==False:
                return {"completed": False, "reason": "No Password Headers"}, 500
            else:
                password = request.headers.get("password")
                db["properties"]["users"][user] = generate_password_hash(password)
                return {"completed": True}, 201

        @self.api.route("/drivers")
        @auth.login_required
        def list_drivers():
            prod = []
            for i in workers.plugin_inst:
                prod.append(i.name)
            return jsonify(prod)

        @self.api.route("/drivers/delete/<driver>")
        @auth.login_required
        def delete_driver(driver):
            chosen = False

            for i in workers.plugin_inst:
                if i.name == driver:
                    chosen = i

            if chosen == False:
                return {"completed": False, "reason": "That Plugin does not exist"}, 500
            elif chosen.name == "OpenLoop Saver":
                return {"completed": False, "reason": "You cannot delete a internal Plugin"}, 500
            else:
                os.remove(f"plugin/{chosen.name}.pyl")
                return {"completed": True}

        @self.api.route("/drivers/upload/<name>", methods=["POST"])
        @auth.login_required
        def upload_driver(name):
            url = request.headers.get("url", None)
            data = requests.get(url)
            if url==None:
                return {"completed": False, "reason": "Url not found in headers"}, 500
            if data.ok:
                with open(f"plugins/{name}.pyl", "w") as f:
                    f.write(data.text)
                return {"completed": True}
            else:
                return {"completed": False, "reason": "Url not accesable"}, 500
        
        @self.api.route("/clear_notifications")
        @auth.login_required
        def notifications():
            alerts.reset()
            return {"completed": True}

        @self.api.route("/pl/<plugin>/<func>", methods=["GET", "POST"])
        def register_function(plugin, func):
            chosen = None
            for i in workers.plugin_inst:
                if i.name == plugin:
                    chosen = i
            if chosen == None:
                return {"completed": False, "reason": "Plugin name does not exist or is Invalid"}, 500
            else:
                
                crossflow.cross_prompt.set_data(func, request.values.get("send", None))

                button = None
                for i in chosen.crossweb.buttons:
                    if str(func) == str(i.id):
                        button = i
                
                if button.onclick == None:
                    return {"completed": False, "reason": "Functionality Missing!"}, 500
                else:
                    if button.onclick != False:
                        x = button.onclick()
                    else:
                        x = None

                    if "\prompt:" in x:
                        return {"completed": True, "return": {"type": "prompt", "data": x.replace("\prompt:", "")}}

                    return {"completed": True, "return": {"type": "message", "data": x}}