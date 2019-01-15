import json
import re
from json import JSONEncoder, JSONDecoder


class Mention:
    """ Contained in a sentence object """
    def __init__(self, sentence, name, mention_type, start, end):
        self.sentence = sentence
        self.type = mention_type
        self.name = name
        self.start = start
        self.end = end
        self.page = sentence.page_num


class Relation:
    """ Contained in a sentence object """
    def __init__(self, main_mention, other_mention):
        self.mention1 = main_mention
        self.mention2 = other_mention
        self.type = f"{main_mention}_{other_mention}".lower()
