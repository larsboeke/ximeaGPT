import datetime
class Text:
    def __init__(self):
        self.metadata = {"type": "text",
                         "source_id": f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                         "document_date": f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                         }
    
    def get_metadata(self):
        return self.metadata