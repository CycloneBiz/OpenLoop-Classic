import os
from openloop.virtualizer import IOT

class WorkerHandler:
    def __init__(self, db) -> None:
        print("Scanning...")
        plugins = os.listdir("plugins")

        # Just for debuging
        print("Found: ", end="")
        for i in plugins:
            print(f"{i.split('.')[0]}, ", end="")
        print()

        self.plugin_inst = []

        names = []
        for i in plugins:
            name = i.split('.')[0]
            if name in names:
                print("Theres more than one file with the same initial name!")
            print(f"Starting {name} daemon(s)...")
            with open(f"plugins/{i}") as f:
                past_data = db["plugin_data"].get(name, {})
                self.plugin_inst.append(IOT(name, db, past_data, f.read()))
            