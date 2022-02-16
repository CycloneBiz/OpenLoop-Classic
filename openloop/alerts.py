from datetime import datetime

class Alert:
    def __init__(self, icon, name, description, color) -> None:
        self.icon = icon
        self.name = name
        self.description = description
        self.hour = datetime.now().time().hour
        self.minute = datetime.now().time().minute
        self.date = str(datetime.now().date())
        self.combo = f"{self.date} {self.hour}:{self.minute}"
        self.color = color
    def __repr__(self) -> str:
        return f"Alert(\"{self.icon}\", \"{self.name}\"))"

class AlertManager(list):
    def __init__(self):
        super().__init__()

    def reset(self):
        super().__init__() # Reinitializes the list object

    def submit(self, object):
        self.insert(0, object)

    def length(self):
        return len(self)