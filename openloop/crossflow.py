class CrossPrompt(dict):
    def __init__(self) -> None:
        super().__init__()
    
    def get_data(self, fn):
        return self.get(fn, None)

    def set_data(self, fn, string):
        self[fn] = string

    def data_used(self, fn):
        self.pop(fn)

class MemoryManager:
    def __init__(self) -> None:
        self.requires = {}

    def register(self, libname, lib):
        if libname in self.requires:
            with open("errors.log", "a") as f:
                f.write(f"Two registered libs ({libname}) have the same name, only using the first selected")
        else:
            self.requires[libname] = lib

    def get(self, libname):
        if not libname in self.requires:
            raise ImportWarning(f"Could not find the package {libname}")
        else:
            return self.requires[libname]

class FrontButton:
    def __init__(self, title, color, icon, value = "NaN") -> None:
        self.title = title
        self.color = color
        self.icon = icon
        self.value = value

class DashPanel:
    def __init__(self) -> None:
        self.dash_buttons = [FrontButton("Example Section", "text-success", "fab fa-superpowers"), FrontButton("Example Section", "text-info", "fas fa-clipboard-list")]
        self.button = FrontButton

class CrossFlow:
    def __init__(self) -> None:
        self.cross_prompt = CrossPrompt()
        self.memory = MemoryManager()
        self.dash = DashPanel()