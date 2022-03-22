from openloop.virtualizer import Database
import os

db = Database()
db.restore()

if os.path.exists("errors.log"):
    os.remove("errors.log")

# CrossFlow
from openloop.crossflow import CrossFlow
crossflow = CrossFlow()

# Alert System
from openloop.alerts import AlertManager
alerts = AlertManager()

print("Runing plugin emulation...")
# Enable Plugins and Workers
from openloop.workers import WorkerHandler
worker_handle = WorkerHandler(db, alerts, crossflow)

if os.path.exists("errors.log"):
    with open("errors.log") as f:
        data = f.read().split("\n")
    for i in data:
        print(i)
else:
    print("No errors compiling...")

print("Launch site completed... feel free to exit now")