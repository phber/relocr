from pymongo import MongoClient
import spacy
import unidecode
from decimal import Decimal
from bson.decimal128 import Decimal128

nlp = spacy.load('en')

client = MongoClient('localhost', 27017)
db = client['off']


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def store_ingredients():
    tags = db.products.aggregate([{"$group": {"_id": "$ingredients_tags"}}], allowDiskUse=True, no_cursor_timeout=True)
    for d in tags:
        if d['_id']:
            for t in d['_id']:
                if ':' not in t:
                    continue
                _, ing = t.split(':')
                if len(ing) < 3:
                    continue
                if hasNumbers(ing):
                    continue
                ing = ing.replace('-', ' ')
                res = db['ingredients'].find_one({'name': ing})
                if not res:
                    db['ingredients'].insert_one({'name': ing, 'count': 1})
                else:
                    db['ingredients'].update({'_id': res['_id']}, {'$inc': {'count': 1}})

def store_categories():
    tags = db.products.aggregate([{"$group": {"_id": "$categories"}}], allowDiskUse=True)
    for r in tags:
        if not r['_id']:
            continue
        for part in r['_id'].split(','):
            res = db['categories'].find_one({'name': part.strip()})
            if not res:
                db['categories'].insert_one({'name': part.strip(), 'count': 1})
            else:
                db['categories'].update({'_id': res['_id']}, {'$inc': {'count': 1}})



#store_categories()
db.ingredients.delete_many({'count': {'$lt': 10}})