from .db_utils import db
from relocr.utils.textual import get_capitalized_parts, top_ngrams
from unidecode import unidecode
from nltk.stem.wordnet import WordNetLemmatizer

lmtzr = WordNetLemmatizer()


def db_find_products(document):
    sents = document.get_sentences()
    caps = get_capitalized_parts(sents)
    top = top_ngrams(caps, ngram_range=(2, 6))
    top.sort(key=lambda x: len(x.split()), reverse=True)  # Sort by number of grams
    res = []
    matched_phrases = []
    for cand_phrase in top:
        if any(cand_phrase.lower() in match.lower() for match in matched_phrases):
            continue
        query = {'$text': {'$search': f'\"{cand_phrase}\""'}}
        proj = {'product_name': 1, 'brands': 1, 'score': {'$meta': 'textScore'}}
        found = db['products'].find(query, projection=proj).sort([('score', {'$meta': 'textScore'})]).limit(1)
        for r in found:
            if unidecode(r['product_name'].lower()) == cand_phrase:
                res.append(cand_phrase)
                matched_phrases.append(cand_phrase)
    return res


def db_find_categories(document):
    sents = document.get_sentences()
    top = top_ngrams(sents, ngram_range=(1, 3), min_freq=2)
    top.sort(key=lambda x: len(x.split()), reverse=True)  # Sort by number of grams
    res = []
    matched_phrases = []
    top = [x for x in top if not any(c.isdigit() for c in x)]  # Filter categories without digits
    top = [x for x in top if len(x) > 2]  # Longer than 2
    print(top)
    for cand_phrase in top:
        if any(cand_phrase.lower() in match.lower() for match in matched_phrases):
            continue
        query = {'$text': {'$search': f'\"{cand_phrase}\""'}}
        proj = {'name': 1, 'score': {'$meta': 'textScore'}}
        found = db['categories'].find(query, projection=proj).sort([('score', {'$meta': 'textScore'})]).limit(1)
        for r in found:
            if lmtzr.lemmatize(r['name'].lower()) == lmtzr.lemmatize(cand_phrase):
                res.append(cand_phrase)
                matched_phrases.append(cand_phrase)
    return res


def get_all(document):
    sents = document.get_sentences()
    caps = get_capitalized_parts(sents)
    top = top_ngrams(caps)
    top.sort(key=lambda x: len(x.split()), reverse=True)  # Sort by number of grams
