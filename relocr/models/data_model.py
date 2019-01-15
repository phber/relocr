import json
from json import JSONEncoder, JSONDecoder
import logging
import spacy
from .relation_model import Mention, Relation
import re
from collections import defaultdict

nlp = spacy.load('en')


class DocumentEncoder(JSONEncoder):
    def default(self, o):  # pylint: disable=E0202
        if isinstance(o, TextBox):
            res = o.__dict__.copy()
            res.pop('sentences')
            return res
        return o.__dict__


class SentenceEncoder(JSONEncoder):
    """ For debugging purposes """
    def default(self, o):  # pylint: disable=E0202
        if isinstance(o, Sentence):
            if o.mentions == []:
                return {}
            res = {}
            res['text'] = o.text
            res['bbox'] = (o.left, o.bottom, o.right, o.top)
            res['mentions'] = []
            for m in o.mentions:
                res['mentions'].append({'type': m.type, 'start': m.start, 'end': m.end, 'text': m.text})
            res['relations'] = []
            for r in o.relations:
                res['relations'].append({'type': r.type, 'mention1': r.mention1.name, 'mention2': r.mention2.name})
            return res
        return o.__dict__


class Document:
    def __init__(self, title, pages=[]):
        self.title = title
        self.pages = pages
        self.entity_dict = None

    def get_page(self, num):
        for p in self.pages:
            if p['num'] == num:
                return p
        raise ValueError(f"No page with number {num}.")

    def get_sentences(self, form='object'):
        res = []
        for p in self.pages:
            for b in p.boxes:
                for s in b.sentences:
                    if 'lemma' in form:
                        res.append(' '.join(s.lemmas))
                    elif 'text' in form:
                        res.append(s.text)
                    else:
                        res.append(s)
        if res == []:
            logging.warn('No sentences in document. Make sure document.parse() has been called.')
        return res

    def parse_sentences(self):
        for p in self.pages:
            for b in p.boxes:
                for sent in nlp(b.text).sents:
                    s = Sentence(p.num, sent, (b.left, b.bottom, b.right, b.top))
                    b.sentences.append(s)

    def parse_mentions(self):
        if not self.entity_dict:
            logging.warn("Not parsing mentions since entity_dict is None.")
            return
        for sent in self.get_sentences():
            lemmas = ' '.join(sent.lemmas)
            for typ, cands in self.entity_dict.items():
                for key in cands.keys():
                    rx = re.compile(r'\b' + key + r'\b', re.IGNORECASE)
                    found = re.search(rx, lemmas)
                    if found:
                        m = Mention(lemmas, key, typ, found.start(), found.end())
                        sent.mentions[typ].append(m)

    def __repr__(self):
        return json.dumps(self, cls=DocumentEncoder, indent=4)

    @staticmethod
    def from_json(json_object):
        if isinstance(json_object, str):
            json_object = json.loads(json_object)
        d = Document(json_object['title'])
        d.entity_dict = json_object['entity_dict']
        for p in json_object['pages']:
            page = Page(p['num'], (0, 0, p['x'], p['y']))
            for box in p['boxes']:
                bbox = (box['left'], box['bottom'], box['right'], box['top'])
                page.boxes.append(TextBox(box['num'], bbox, box['text']))
            d.pages.append(page)
        return d


class Page:
    def __init__(self, num, bbox):
        self.num = num
        self.boxes = []
        self.x = round(bbox[2])  # right
        self.y = round(bbox[3])  # top

    def get_mentions(self, typ):
        res = []
        for box in self.boxes:
            for sent in box.sentences:
                res.extend(sent.mentions[typ])
        return res

    def get_sentences(self, form='object'):
        res = []
        for b in self.boxes:
            for s in b.sentences:
                if 'lemma' in form:
                    res.append(' '.join(s.lemmas))
                elif 'text' in form:
                    res.append(s.text)
                else:
                    res.append(s)
        return res


class TextBox:
    def __init__(self, num, bbox, text):
        self.num = num
        # PDF Coordinates have origin in lower left corner of the page
        self.left = round(bbox[0])
        self.bottom = round(bbox[1])
        self.right = round(bbox[2])
        self.top = round(bbox[3])
        self.text = text
        self.sentences = []


class Sentence:
    """ Contained in TextBox"""
    def __init__(self, page_num, span, textbox):
        self.page_num = page_num
        self.text = span.text
        self.lemmas = [token.lemma_ for token in span]
        self.pos = [token.pos_ for token in span]
        self.left = textbox.left
        self.bottom = textbox.bottom
        self.right = textbox.right
        self.top = textbox.top
        self.textbox = textbox
        self.mentions = defaultdict(list)
        self.relations = []

    def __repr__(self):
        return json.dumps(self, cls=SentenceEncoder, indent=4)