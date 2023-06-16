class URL:
    def __init__(self, path):
        self.path = path
        self.metadata = {"type": "manuals","source": path}

    def get_path(self):
        return self.path
    
    def get_metadata(self):
        return self.metadata