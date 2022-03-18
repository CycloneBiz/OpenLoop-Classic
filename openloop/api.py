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
                value = request.values.get("send", None)
                if value == "null":
                    value = None
                
                crossflow.cross_prompt.set_data(func, value)

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

                    if "\prompt:" in str(x):
                        return {"completed": True, "return": {"type": "prompt", "data": x.replace("\prompt:", "")}}

                    return {"completed": True, "return": {"type": "message", "data": x}}