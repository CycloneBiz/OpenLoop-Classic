from flask import Flask
from openloop.virtualizer import Database

from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)

auth = HTTPBasicAuth()

db = Database()
db.restore()

from openloop.auth import Auth_Handler
auth_handle = Auth_Handler(db, auth)

# Enable Plugins and Workers
from openloop.workers import WorkerHandler
print(" * Turning on Plugin Support... ")
worker_handle = WorkerHandler(db)

# Setup Save Handler
from openloop.saver import WorkSaveHandler
print(" * Turning on Plugin Save Support... ")
save_handler = WorkSaveHandler(worker_handle, db["properties"]["autosave"]["work_save"], db)

# Import Web Interface System
from openloop.web import Web_Handler
web_handler = Web_Handler(db, worker_handle, auth)
app.register_blueprint(web_handler.web, url_prefix="/")
print(" * Website System Imported...")

# Import API and share database
from openloop.api import API_Handler
api_handler = API_Handler(db, worker_handle, auth)
app.register_blueprint(api_handler.api, url_prefix="/api")
print(" * API Imported...")

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)