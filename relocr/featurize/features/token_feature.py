import re
from relocr.featurize.feature_model import AbstractFeature


class HeadFeature(AbstractFeature):
    @staticmethod
    def get_head(sentence, start, end):
        head = end - 1
        for i in range(start, end):
            pt = sentence.pos[i]
            if pt.startswith('N'):
                head = i
            elif pt == 'IN' or pt == ',':
                break
        return head

    def apply(self, mention1, mention2, features):
        em1index = HeadFeature.get_head(mention1.sentence, mention1.start, mention1.end)
        features.append('HEAD_EM1_%s' % mention1.sentence.lemmas[em1index])
        em2index = HeadFeature.get_head(mention2.sentence, mention1.start, mention2.end)
        features.append('HEAD_EM2_%s' % mention2.sentence.lemmas[em2index])


class EntityMentionTokenFeature(AbstractFeature):
    def apply(self, mention1, mention2, features):
        for i in range(mention1.start, mention1.end):
            features.append('TKN_EM1_%s' % mention1.sentence.lemmas[i])
        for i in range(mention2.start, mention2.end):
            features.append('TKN_EM2_%s' % mention2.sentence.lemmas[i])


class BetweenEntityMentionTokenFeature(AbstractFeature):
    def apply(self, mention1, mention2, features):
        if not mention1.sentence == mention2.sentence:
            return
        sentence = mention1.sentence
        start = mention1.end
        end = mention2.start
        if mention1.start > mention2.start:
            start = mention2.end
            end = mention1.start
        for i in range(start, end):
            if i == start:
                features.append('FIRST_TKN_BTWN_%s' % sentence.lemmas[i])
            if i == (end - 1):
                features.append('LAST_TKN_BTWN_%s' % sentence.lemmas[i])
            features.append('TKN_BTWN_%s' % sentence.lemmas[i])


class ContextFeature(AbstractFeature):
    def __init__(self, window_size=1):
        self.window_size = window_size

    def apply(self, mention1, mention2, features):
        sentence = mention1.sentence
        for i in range(max(0, mention1.start - self.window_size), mention1.start):
            features.append('CTXT_EM1_LEFT_%s' % sentence.lemmas[i])
        for i in range(mention1.end, min(sentence.size(), mention1.end + self.window_size)):
            features.append('CTXT_EM1_RIGHT_%s' % sentence.lemmas[i])
        for i in range(max(0, mention2.start - self.window_size), mention2.start):
            features.append('CTXT_EM2_LEFT_%s' % sentence.lemmas[i])
        for i in range(mention2.end, min(sentence.size(), mention2.end + self.window_size)):
            features.append('CTXT_EM2_RIGHT_%s' % sentence.lemmas[i])


class PosFeature(AbstractFeature):
    def apply(self, mention1, mention2, features):
        if not mention1.sentence == mention2.sentence:
            return
        sentence = mention1.sentence
        start = mention1.end
        end = mention2.start
        if mention1.start > mention2.start:
            start = mention2.end
            end = mention1.start
        for i in range(start, end):
            features.append('POS_%s' % sentence.pos[i])


class DistanceFeature(AbstractFeature):
    def apply(self, mention1, mention2, features):
        if not mention1.sentence == mention2.sentence:
            return
        if mention2.start > mention1.start:
            dist = mention2.start - mention1.end
        elif mention2.start < mention1.start:
            dist = mention1.start - mention2.end
        features.append('DISTANCE_%d' % dist)


class EntityMentionOrderFeature(AbstractFeature):
    def apply(self, mention1, mention2, features):
        if not mention1.sentence == mention2.sentence:
            return
        if mention1.start < mention2.start:
            features.append('EM1_BEFORE_EM2')
        elif mention1.start > mention2.start:
            features.append('EM2_BEFORE_EM1')
