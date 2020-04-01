from .basecontroller import BaseController

class LogFilesController(BaseController):
    def __init__(self):
        super().__init__() 

    def update(self, **kwargs): 
        if kwargs['action'] == 'add': 
            for view in self.views: 
                view.addToTable(kwargs['data'])    