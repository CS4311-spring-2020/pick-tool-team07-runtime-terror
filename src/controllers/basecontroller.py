class BaseController(object): 
    def __init__(self):
        self.views = []

    def register(self, view): 
        self.views.append(view)

    def update(self, **kwargs): 
        pass
    
