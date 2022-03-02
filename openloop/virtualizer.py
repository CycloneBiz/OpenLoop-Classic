import threading, time
from datetime import datetime

from openloop.store import backup, restore
from openloop.alerts import Alert
from openloop.crossweb import CrossWeb, Element, Container, Row

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
    def __init__(self, name, superbase, crossflow, database = {}, data = None, alerts = [], path=None) -> None:
        self.crossweb = CrossWeb()
        self.crossflow = None
        self.working = True
        self.feature = {}
        self.settings = {
        }
        self.name = name
        self.database = database

        if path == None:
            self.path = name
        else:
            self.path = path

        if data == None:
            with open(name) as f:
                script = f.read()
        else:
            script = data
        global_vars = {
            "io": self,
            "database": superbase,
            "AlertManager": alerts,
            "Alert": Alert,
            "crossweb": self.crossweb,
            "Element": Element,
            "Container": Container,
            "Row": Row,
            "CrossPrompt": crossflow.cross_prompt
        }
        try:
            exec(compile(script, name, "exec"), global_vars, {})
        except Exception as e:
            with open("errors.log", "a") as f:
                self.working = False
                f.write(str(e.args)+"\n")
    
    def publish(self, subbase, object):
        if not subbase in self.database:
            self.database[subbase] = []
        else:
            self.database[subbase].append(object)

    def runtime(self, func, ms):
        while self.running:
            try:
                func()            
            except Exception as e:
                with open("errors.log", "a") as f:
                    f.write(str(e.args)+"\n")
                self.working = False
            time.sleep(ms / 1000)
        
    def worker(self, func, ms):
        thread = threading.Thread(target=self.runtime, args=[func, ms])
        thread.start()
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