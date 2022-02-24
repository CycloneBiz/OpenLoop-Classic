class Button:
    def __init__(self, name, color = "secondary", icon="fas fa-infinity", onclick=None, id=None):
        self.onclick = onclick
        self.name = name
        self.color = color
        self.icon = icon
        if id == None:
            self.id = name
        else:
            self.id = id
        
    def __repr__(self) -> str:
        return self.name

class ButtonList(list):
    def __init__(self):
        super().__init__()

    def preset(self):
        self.append(Button("Calibrate", icon="fas fa-redo"))
        self.append(Button("Restart", icon="fas fa-exclamation-triangle"))
        self.append(Button("Purge", icon="fas fa-trash"))

    def clear(self):
        super().__init__()
        
    def scan(self, name):
        for i in self:
            if i.name == name:
                return i

class CrossWeb:
    def __init__(self) -> None:
        self.buttons = ButtonList()
        self.button = Button
