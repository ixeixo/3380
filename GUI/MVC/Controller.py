class Controller:
    def __init__(self, model, view, theHash):
        self.model = model
        self.view = view
        self.hash = theHash
        
        self.fileName = ""


    def SendFile(self):
        self.hash.startHash()

    def SetFile(self, filename):
        self.fileName = filename


    def GetFile(self):
        return self.fileName


    def GetMatch(self):
        return


