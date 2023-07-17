import datetime
class Text:
    def __init__(self):
        self.metadata = {"type": "text",
                         "source_id": f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                         "document_date": f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                         }
    
    def get_metadata(self):
        """
        Returns the metadata of the text
        :return metadata:
        """
        return self.metadata