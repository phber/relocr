from relocr.models.relation_model import Relation


class Labeler:
    def __init__(self, documents, main_type, second_type, labeling_fns):
        self.docs = documents
        self.fns = labeling_fns
        self.type1 = main_type
        self.type2 = second_type

    def apply_doc(self, doc):
        for sent in doc.get_sentences():
            for mention1 in sent.mentions[self.type1]:
                for mention2 in sent.mentions[self.type2]:
                    indicator = 0
                    for fn in self.fns:
                        indicator += fn(doc, mention1, mention2)
                    if indicator > 0:
                        sent.relations.append(Relation(mention1, mention2))

    def apply(self):
        for doc in self.docs:
            self.apply_doc(doc)
        return self.docs



