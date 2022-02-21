class Button:
    def __init__(self, name, color = "secondary", icon="fa-infinity"):
        self.onclick = None
        self.name = name
        self.color = color
        self.icon = icon
    def __repr__(self) -> str:
        return self.name

class ButtonList(list):
    def __init__(self):
        super().__init__()
        self.append(Button("Calibrate", icon="fa-redo"))
        self.append(Button("Restart", icon="fa-exclamation-triangle"))
        self.append(Button("Purge", icon="fa-trash"))

class CrossWeb:
    def __init__(self) -> None:
        self.buttons = ButtonList()