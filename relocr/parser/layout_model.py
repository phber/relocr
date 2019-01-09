import json
import logging


class Document:
    def __init__(self, title, pages=[]):
        self.title = title
        self.pages = pages

    def get_sentences(self):
        sents = []
        for page in self.pages:
            for box in page.boxes:
                for sent in box.text.split('.'):
                    sents.append(sent)
        return sents

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    @classmethod
    def from_json(cls, s):
        json_dict = json.loads(s)
        return cls(**json_dict)


class Page:
    def __init__(self, num, bbox):
        self.num = num
        self.boxes = []
        self.x = round(bbox[2])  # right
        self.y = round(bbox[3])  # top


class TextBox:
    def __init__(self, num, bbox, text):
        self.num = num
        # PDF Coordinates have origin in lower left corner of the page
        self.left = round(bbox[0])
        self.bottom = round(bbox[1])
        self.right = round(bbox[2])
        self.top = round(bbox[3])
        self.text = text
