class AbstractFeature(object):
    def apply(self, sentence, mention, features):
        raise NotImplementedError()