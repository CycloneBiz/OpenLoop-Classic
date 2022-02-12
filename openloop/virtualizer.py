import threading, time
from datetime import datetime

from openloop.store import backup, restore
from openloop.alerts import Alert

class Database(dict):
    size = 0
    def save(self):
        self.size = backup(self)
        return self.size

    def restore(self):
        self.update(restore())

class IOT:
    threads = []
    running = True
    feature = {}
    settings = {
        "icon": "fas fa-plug"
    }
    def __init__(self, name, superbase, database = {}, data = None, alerts = []) -> None:
        self.name = name
        self.database = database
        if data == None:
            with open(name) as f:
                script = f.read()
        else:
            script = data
        
        exec(script, {"io": self, "database": superbase, "AlertManager": alerts, "Alert": Alert}, {})
    
    def publish(self, subbase, object):
        if not subbase in self.database:
            self.database[subbase] = []
        else:
            self.database[subbase].append(object)

    def runtime(self, func, ms):
        while self.running:
            func()
            time.sleep(ms / 1000)
        
    def worker(self, func, ms):
        thread = threading.Thread(target=self.runtime, args=[func, ms])
        thread.start()
        print(f"Started thread for function {func}")
        self.threads.append(thread)

    def extract_features(self):
        prod = {}
        for i in self.feature:
            prod[i] = self.database.get(self.feature[i], [])
        return prod

    def generate_origin(self):
        self.publish("origin", str(datetime.now().date()))
        if not "origin" in self.feature:
            self.feature["origin"] = "origin"