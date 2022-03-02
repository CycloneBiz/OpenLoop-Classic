class CrossPrompt(dict):
    def __init__(self) -> None:
        super().__init__()
    
    def get_data(self, fn):
        return self.get(fn, None)

    def set_data(self, fn, string):
        self[fn] = string

    def data_used(self, fn):
        self.pop(fn)

class CrossFlow:
    def __init__(self) -> None:
        self.cross_prompt = CrossPrompt()