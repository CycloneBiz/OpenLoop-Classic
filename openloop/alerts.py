class Alert:
    def __init__(self, icon, name, description) -> None:
        self.icon = icon
        self.name = name
        self.description = description
    def __repr__(self) -> str:
        return f"Alert(\"{self.icon}\", \"{self.name}\"))"

class AlertManager(list):
    pass