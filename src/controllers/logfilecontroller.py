from .basecontroller import BaseController

class LogFilesController(BaseController):
    def __init__(self):
        super().__init__() 

    # Dont really like this implementation
    # I am thinking of having a base class where all "Widgets/Views"
    # inherite from and override some update function
    # to do what ever is needed to be done. For now this should work
    def update(self, **kwargs): 
        if kwargs['action'] == 'add': 
            for view in self.views: 
                view.addToTable(kwargs['data'])    