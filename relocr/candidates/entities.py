import json
import spacy
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.oauth2 import service_account


def match_type(text):
    """Detects entities in the text."""
    credentials = service_account.Credentials.from_service_account_file('gcloud_service.json')
    client = language.LanguageServiceClient(credentials=credentials)

    # Instantiates a plain text document.
    document = types.Document(
        content=text.lower(),
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities

    # entity types from enums.Entity.Type
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

    res = []
    for entity in entities:
        if entity.name in res:
            continue
        if entity_type[entity.type] not in ['CONSUMER_GOOD']:
            continue
        if entity.salience < 10**(-4):
            continue
        res.append(entity.name)
    return res

def match(text):
    nlp = spacy.load('en')
    doc = nlp(text)
    for ent in doc.ents:
        print(ent.text, ent.label_)

with open('test.json') as f:
    data = f.read()

d = json.loads(data)
text = d['content'].replace('\n', '').lower()
match(text)