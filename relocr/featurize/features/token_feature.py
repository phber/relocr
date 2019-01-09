import re
from abstract_feature import AbstractFeature


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

    def apply(self, sentence, mention, features):
        em1index = HeadFeature.get_head(sentence, mention.em1Start, mention.em1End)
        features.append('HEAD_EM1_%s' % sentence.lemmas[em1index])
        em2index = HeadFeature.get_head(sentence, mention.em2Start, mention.em2End)
        features.append('HEAD_EM2_%s' % sentence.lemmas[em2index])


class EntityMentionTokenFeature(AbstractFeature):
    def apply(self, sentence, mention, features):
        for i in range(mention.em1Start, mention.em1End):
            features.append('TKN_EM1_%s' % sentence.lemmas[i])
        for i in range(mention.em2Start, mention.em2End):
            features.append('TKN_EM2_%s' % sentence.lemmas[i])


class BetweenEntityMentionTokenFeature(AbstractFeature):
    def apply(self, sentence, mention, features):
        start = mention.em1End
        end = mention.em2Start
        if mention.em1Start > mention.em2Start:
            start = mention.em2End
            end = mention.em1Start
        for i in range(start, end):
            if i == start:
                features.append('FIRST_TKN_BTWN_%s' % sentence.lemmas[i])
            if i == (end - 1):
                features.append('LAST_TKN_BTWN_%s' % sentence.lemmas[i])
            features.append('TKN_BTWN_%s' % sentence.lemmas[i])


class ContextFeature(AbstractFeature):
    def __init__(self, window_size=1):
        self.window_size = window_size

    def apply(self, sentence, mention, features):
        for i in range(max(0, mention.em1Start - self.window_size), mention.em1Start):
            features.append('CTXT_EM1_LEFT_%s' % sentence.lemmas[i])
        for i in range(mention.em1End, min(sentence.size(), mention.em1End + self.window_size)):
            features.append('CTXT_EM1_RIGHT_%s' % sentence.lemmas[i])
        for i in range(max(0, mention.em2Start - self.window_size), mention.em2Start):
            features.append('CTXT_EM2_LEFT_%s' % sentence.lemmas[i])
        for i in range(mention.em2End, min(sentence.size(), mention.em2End + self.window_size)):
            features.append('CTXT_EM2_RIGHT_%s' % sentence.lemmas[i])
