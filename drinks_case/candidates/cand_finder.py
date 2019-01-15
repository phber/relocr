from .db_utils import db
from relocr.utils.textual import get_capitalized_parts, top_ngrams
import re
from unidecode import unidecode


def db_find_products(document, brands=[]):
    sents = document.get_sentences('text')
    caps = get_capitalized_parts(sents)
    top = top_ngrams(caps, ngram_range=(1, 6))
    top = [x for x in top if len(x) > 3]  # Longer than 2
    top.sort(key=lambda x: len(x.split()), reverse=False)  # Sort by number of grams
    res = {}
    #  brand_regex = re.compile(f"{'|'.join(brands)}", re.IGNORECASE)
    for cand_phrase in top:
        #  query = {'$and': [{'brands': brand_regex}, {'$text': {'$search': f'\"{cand_phrase}\""'}}]}
        query = {'$text': {'$search': f'\"{cand_phrase}\""'}}
        proj = {'product_name': 1, 'brands': 1, 'score': {'$meta': 'textScore'}}
        found = db['products'].find(query, projection=proj).sort([('score', {'$meta': 'textScore'})]).limit(1)
        for r in found:
            if unidecode(r['product_name']).lower() != unidecode(cand_phrase).lower():
                continue
            res[cand_phrase] = {'synonyms': []}
    return res


def db_find_categories(document):
    sents = document.get_sentences('lemma')
    top = top_ngrams(sents, ngram_range=(1, 3), min_freq=3)
    top.sort(key=lambda x: len(x.split()), reverse=False)  # Sort by number of grams
    res = res = {}
    top = [x for x in top if not any(c.isdigit() for c in x)]  # Filter categories without digits
    top = [x for x in top if len(x) > 2]  # Longer than 2
    for cand_phrase in top:
        query = {'$text': {'$search': f'\"{cand_phrase}\""'}}
        proj = {'name': 1, 'score': {'$meta': 'textScore'}}
        found = db['categories'].find(query, projection=proj).sort([('score', {'$meta': 'textScore'})]).limit(1)
        for r in found:
            if r['score'] < 1:
                break
            matched = False
            for k in res.keys():
                if k in cand_phrase:
                    res[k]['synonyms'].append(cand_phrase)
                    matched = True
                    break
            if not matched:
                res[cand_phrase] = {'synonyms': []}
    return res


def db_find_ingredients(document):
    sents = document.get_sentences('lemma')
    top = top_ngrams(sents, ngram_range=(1, 3), min_freq=2)
    top.sort(key=lambda x: len(x.split()), reverse=False)  # Sort by number of grams
    res = {}
    top = [x for x in top if not any(c.isdigit() for c in x)]  # Filter categories without digits
    top = [x for x in top if len(x) > 2]  # Longer than 2
    for cand_phrase in top:
        query = {'$text': {'$search': f'\"{cand_phrase}\""'}}
        proj = {'name': 1, 'score': {'$meta': 'textScore'}}
        found = db['ingredients'].find(query, projection=proj).sort([('score', {'$meta': 'textScore'})]).limit(1)
        for r in found:
            if r['score'] < 1:
                break
            matched = False
            for k in res.keys():
                if k in cand_phrase:
                    res[k]['synonyms'].append(cand_phrase)
                    matched = True
                    break
            if not matched:
                res[cand_phrase] = {'synonyms': []}
    return res


def parse_candidates(doc):
    doc.parse()
    prods = db_find_products(doc)
    ings = db_find_ingredients(doc)
    cats = db_find_categories(doc)
    for prod in prods:
        if prod in ings or prod in cats:
            prods.pop(prod)   # Remove brands that are ingredients or categories
    d = {'products': prods, 'ingredients': ings, 'categories': cats}
    doc.entity_dict = d
