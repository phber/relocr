import json


class Document:
    def __init__(self, title, pages=[]):
        self.title = title
        self.pages = pages

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


class Page:
    def __init__(self, num, bbox):
        self.num = num
        self.areas = []
        self.x = bbox[2]  # right
        self.y = bbox[3]  # top

    def get_sentences(self):
        for area in self.areas:
            for para in area.paragraphs:
                for sentence in para.sentences:
                    yield sentence


class Area:
    def __init__(self, num, bbox):
        self.num = num
        self.left = bbox[0]
        self.bottom = bbox[1]
        self.right = bbox[2]
        self.top = bbox[3]
        self.paragraphs = []


class Sentence:
    """ Contained in Paragraph object """
    def __init__(self, tokens=[]):
        self.tokens = tokens
        self.left = 100000
        self.bottom = 100000
        self.right = -100000
        self.top = -100000

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


class Paragraph:
    def __init__(self, num, bbox):
        self.num = num
        self.left = bbox[0]
        self.bottom = bbox[1]
        self.right = bbox[2]
        self.top = bbox[3]
        self.lines = []
        self.sentences = []

    def parse_sentences(self):
        if len(self.sentences) > 0:
            raise ValueError("Sentences for paragraph are already parsed.")
        cur_sent = Sentence()
        for line in self.lines:
            if line.left < cur_sent.left:
                cur_sent.left = line.left
            if line.right > cur_sent.right:
                cur_sent.right = line.right
            if line.top > cur_sent.top:
                cur_sent.top = line.top
            if line.bottom < cur_sent.bottom:
                cur_sent.bottom = line.bottom
            for tok in line.words:
                if tok[-1] == '.':
                    cur_sent.tokens.append(tok.replace('.', ''))
                    cur_sent.tokens.append('.')
                    self.sentences.append(cur_sent)
                    cur_sent = Sentence()
                else:
                    cur_sent.tokens.append(tok)


class Line:
    def __init__(self, num, bbox, words=[]):
        self.num = num
        self.bbox = bbox
        self.left = bbox[0]
        self.bottom = bbox[1]
        self.right = bbox[2]
        self.top = bbox[3]
        self.words = words
