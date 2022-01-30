from time import sleep
import threading

class WorkSaveHandler:
    def __init__(self, worker_handler, ms, db) -> None:
        self.thread = threading.Thread(target=self.handler, args=[worker_handler, ms, db])
        self.thread.start()

    def handler(self, worker_handler, ms, db):
        while True:
            sleep(ms/1000)
            for i in worker_handler.plugin_inst:
                db["plugin_data"][i.name] = i.database
            