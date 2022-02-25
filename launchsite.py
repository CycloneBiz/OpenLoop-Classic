from openloop.virtualizer import Database

db = Database()
db.restore()

# Alert System
from openloop.alerts import AlertManager
alerts = AlertManager()

print("Runing plugin emulation...")
# Enable Plugins and Workers
from openloop.workers import WorkerHandler
worker_handle = WorkerHandler(db, alerts)

print("Launch site completed... feel free to exit now")