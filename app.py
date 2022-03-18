from flask import Flask, render_template
from openloop.virtualizer import Database

from flask_httpauth import HTTPBasicAuth

from openloop.api import API_Handler
from openloop.web import Web_Handler
from openloop.saver import WorkSaveHandler
from openloop.workers import WorkerHandler
from openloop.alerts import AlertManager
from openloop.auth import Auth_Handler

print("Imported Dependencies...")

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "cache"
app.config["MAX_CONTENT-PATH"] = 128000000 

auth = HTTPBasicAuth()

db = Database()
db.restore()

# Data dealer
from openloop.crossflow import CrossFlow
crossflow = CrossFlow()

# Auth Handler
auth_handle = Auth_Handler(db, auth)

# Alert System
alerts = AlertManager()

# Enable Plugins and Workers
print(" * Turning on Plugin Support... ")
worker_handle = WorkerHandler(db, alerts, crossflow)

# Setup Save Handler
print(" * Turning on Plugin Save Support... ")
save_handler = WorkSaveHandler(worker_handle, db["properties"]["autosave"]["work_save"], db)

# Import Web Interface System
web_handler = Web_Handler(db, worker_handle, auth, alerts, crossflow)
app.register_blueprint(web_handler.web, url_prefix="/")
print(" * Website System Imported...")

# Import API and share database
api_handler = API_Handler(db, worker_handle, auth, alerts, crossflow)
app.register_blueprint(api_handler.api, url_prefix="/api")
print(" * API Imported...")

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)