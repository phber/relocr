import json


class Sentence:
    """ Contained in Paragraph object """
    def __init__(self, tokens=[]):
        self.tokens = tokens

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)
