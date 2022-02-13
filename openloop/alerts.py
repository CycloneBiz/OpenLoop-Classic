from datetime import datetime

class Alert:
    def __init__(self, icon, name, description) -> None:
        self.icon = icon
        self.name = name
        self.description = description
        self.hour = datetime.now().time().hour
        self.minute = datetime.now().time().minute
        self.date = str(datetime.now().date())
    def __repr__(self) -> str:
        return f"Alert(\"{self.icon}\", \"{self.name}\"))"

class AlertManager(list):
    pass