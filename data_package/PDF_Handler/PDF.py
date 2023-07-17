class PDF:
    def __init__(self, path):
        self.path = path
        self.metadata = {"type": "manuals","source_id": path}

    def get_path(self):
        """
        Returns the path of the PDF
        :return path::
        """
        return self.path
    
    def get_metadata(self):
        """
        Returns the metadata of the PDF
        :return metadata:
        """
        return self.metadata