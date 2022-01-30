from flask import Blueprint, jsonify, request
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
                db["properties"]["users"]["admin"] = password
                return {"completed": True}

        @self.api.route("/drivers")
        @auth.login_required
        def list_drivers():
            prod = []
            for i in workers.plugin_inst:
                prod.append(i.name)
            return prod

        @self.api.route("/drivers/delete/<driver>")
        @auth.login_required
        def delete_driver(driver):
            chosen = False

            for i in workers.plugin_inst:
                if i.name == driver:
                    chosen = driver
            
            if chosen.name == "OpenLoop Saver":
                return {"completed": False, "reason": "You cannot delete a internal Plugin"}
            elif not chosen:
                return {"completed": False, "reason": "That Plugin does not exist"}
            else:
                os.remove(f"plugin/{chosen.name}.pyl")
                return {"completed": True}

        @self.api.route("/driver/upload")
        @auth.login_required
        def upload_driver():
            file = request.headers.get("file", None)
            name = request.headers.get("name", None).split("/")
            name = name[len(name)-1]
            if file == None or name == None:
                return {"completed": False, "reason": "Missing Headers"}
            elif name.split(".")[len(name.split("."))-1] != ".pyl":
                return {"completed": False, "reason": "Invalid Filename. All plugins should use .pyl"}
            else:
                with open(f"plugins/{name}", "w") as f:
                    f.write(file)
                return {"completed": True}
                