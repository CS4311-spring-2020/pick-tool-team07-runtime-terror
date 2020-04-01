# **Warning**
# We might run into issues with this implementation in the future
# when we move our managers from holding our data in python lists to mongodb

class BaseController(object): 
    def __init__(self):
        self.views = []

    def register(self, view): 
        self.views.append(view)

    def update(self, **kwargs): 
        pass
    
