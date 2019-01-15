import logging
import os
from relocr.parser.pdf_parser import PDF_Extractor
from relocr.models.data_model import Document
from relocr.labeling.labeler import Labeler
from drinks_case.candidates.cand_finder import parse_candidates


def configure_logging():
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


def parse_pdfs(data_dir, output_dir):
    parser = PDF_Extractor()
    docs = parser.extract_dir(data_dir)
    for d in docs:
        new_path = os.path.join(output_dir, d.title + '.json')
        with open(new_path, 'w') as f:
            f.write((str(d)))


def parse_json(input_dir, output_dir):
    """ Parse sentences and entities from JSON documents """
    parsed_docs = []
    for path in os.listdir(input_dir):
        if not path.endswith('.json'):
            continue
        path = os.path.join(input_dir, path)
        logging.info(f"Parsing data from {path} ...")
        with open(path, 'r') as f:
            s = f.read()
        doc = Document.from_json(s)
        doc.parse_sentences()
        parse_candidates(doc)
        doc.parse_mentions()
        parsed_docs.append(doc)
    return parsed_docs


def parse_relations(output_dir, parsed_docs, main_type, other_type, labeling_fns):
    labeler = Labeler(parsed_docs, main_type, other_type, labeling_fns)
    labeler.apply()
    for d in parsed_docs:
        new_path = os.path.join(output_dir, d.title + '.json')
        with open(new_path, 'w') as f:
            f.write((str(d)))        
   

            
