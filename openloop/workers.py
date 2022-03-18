import os
from openloop.virtualizer import IOT
from openloop.alerts import Alert

class WorkerHandler:
    def __init__(self, db, alerts, crossflow) -> None:
        print("Scanning...")
        plugins = os.listdir("plugins")

        # Just for debuging
        print("Found: ", end="")
        for i in plugins:
            print(f"{i.split('.')[0]}, ", end="")
        print()

        self.plugin_inst = []
        dependencies = []
        for i in plugins:
            if i.endswith(".pyr"):
                plugins.remove(i)
                dependencies.append(i)

        names = []
        for i in dependencies:
            path = i
            name = i.split('.')[0]
            if name in names:
                alerts.submit(Alert("fas fa-exclamation-triangle", "OpenLoop Saver", f"The plugin dependent {name} has a duplicate! This will cause major issues to the OpenLoop plugin system.", "danger"))
            names.append(name)
            with open(f"plugins/{i}") as f:
                past_data = db["plugin_data"].get(name, {})
                self.plugin_inst.append(IOT(name, db, crossflow, past_data, f.read(), alerts, path))
        print("Completed Dependencies...")

        # Plugin Support
        names = []
        for i in plugins:
            path = i
            name = i.split('.')[0]
            if name in names:
                alerts.submit(Alert("fas fa-exclamation-triangle", "OpenLoop Saver", f"The plugin {name} has a duplicate! This will cause major issues to the OpenLoop plugin system.", "danger"))
            names.append(name)
            with open(f"plugins/{i}") as f:
                past_data = db["plugin_data"].get(name, {})
                self.plugin_inst.append(IOT(name, db, crossflow, past_data, f.read(), alerts, path))
        print("Completed Plugins...")
            