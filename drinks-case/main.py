from relocr.parser.pdf_parser import PDF_Extractor
from .candidates.cand_finder import db_find_products, db_find_categories
import logging
import json
from relocr.models.layout_models import Document
import pickle


def configure_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


def process():
    doc = PDF_Extractor().extract_dir('drinks-case/data')[0]
    with open('drinks-case/tmp_data/test.bin', 'wb') as pickle_file:
        pickle.dump(doc, pickle_file)


def load():
    with open('drinks-case/tmp_data/test.bin', 'rb') as f:
        doc = pickle.loads(f.read())
    print(db_find_categories(doc))

process()
load()

# page frequency av ordet, avstånd