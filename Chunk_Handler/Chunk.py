class Chunk:
    def __init__(self, json):
        """
        :param json:
        """
        self.json = json

    def get_json(self):
        """
        Get the json
        :return json: chunk as json
        :rtype: json
        """
        return self.json
    