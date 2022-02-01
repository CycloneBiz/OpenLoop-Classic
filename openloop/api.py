from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
import requests
import os

class API_Handler:
    api = Blueprint("api", __name__, "static", "templates")

    def __init__(self, db, workers, auth) -> None:
        self.db = db

        @self.api.route("/")
        @auth.login_required
        def give_version():
            return {"version": 0.01}

        @self.api.route("/setpass")
        @auth.login_required
        def set_password():
            if request.headers.get("password", False)==False:
                return {"completed": False, "reason": "No Password Headers"}
            else:
                password = request.headers.get("password")
                db["properties"]["users"]["admin"] = generate_password_hash(password)
                return {"completed": True}

        @self.api.route("/setpass/<user>")
        @auth.login_required
        def set_password_specific(user : str):
            if request.headers.get("password", False)==False:
                return {"completed": False, "reason": "No Password Headers"}
            else:
                password = request.headers.get("password")
                db["properties"]["users"][user] = generate_password_hash(password)
                return {"completed": True}

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
                return {"completed": False, "reason": "That Plugin does not exist"}
            elif chosen.name == "OpenLoop Saver":
                return {"completed": False, "reason": "You cannot delete a internal Plugin"}
            else:
                os.remove(f"plugin/{chosen.name}.pyl")
                return {"completed": True}

        @self.api.route("/drivers/upload/<name>", methods=["POST"])
        @auth.login_required
        def upload_driver(name):
            url = request.headers.get("url", None)
            data = requests.get(url)
            if url==None:
                return {"completed": False, "reason": "Url not found in headers"}
            if data.ok:
                with open(f"plugins/{name}.pyl", "w") as f:
                    f.write(data.text)
                return {"completed": True}
            else:
                return {"completed": False, "reason": "Url not accesable"}