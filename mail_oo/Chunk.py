class Chunk:
    def __init__(self, content, metadata):
        self.content = content
        self.metadata = metadata

    def get_content(self):
        return self.content
    
    def get_metadata(self):
        return self.metadata