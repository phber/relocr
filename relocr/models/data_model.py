import json
import spacy


nlp = spacy.load('en')


class Mention:
    """ Contained in a sentence object """
    def __init__(self, sentence):
        self.sentence = sentence
        self.start_index = 0
        self.end_index = 0


class Relation:
    """ Contained in a sentence object """
    def __init__(self):
        pass


class Sentence:
    """ Contained in Paragraph object """
    def __init__(self, tokens):
        self.tokens = nlp(tokens)
        self.lemmas = [token.lemma_ for token in self.tokens]
        self.pos = [token.pos_ for token in self.tokens]
