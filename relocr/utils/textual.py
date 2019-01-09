import unidecode
from nltk import ngrams
from sklearn.feature_extraction.text import CountVectorizer
import spacy


def get_capitalized_parts(sentences):
    """ Returns parts of a sentence that begin with an uppercaser letter """
    all_parts = []
    for sent in sentences:
        part = ''
        for tok in sent.split():
            if tok.isupper():
                if part:
                    all_parts.append(part)
                    part = ''
                continue
            elif tok[0].islower():
                if part:
                    all_parts.append(part)
                    part = ''
                continue
            else:
                part += tok
                part += ' '
        if part:
            all_parts.append(part)
    return all_parts


def top_ngrams(sentences, ngram_range=(1, 5), min_freq=3):
    """ Return list of n-grams with a frequency > min_freq """
    vec = CountVectorizer(ngram_range=ngram_range)
    ngrams = vec.fit_transform(sentences)
    vocab = vec.vocabulary_
    count_values = ngrams.toarray().sum(axis=0)
    res = []
    for ng_count, ng_text in sorted([(count_values[i], k) for k, i in vocab.items()], reverse=True):
        if ng_count < min_freq:
            break
        res.append(ng_text)
    return res


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def get_between_tokens(m1, m2):
    """Return the tokens between two mentions"""
    if m1.sentence != m2.sentence:
        raise ValueError('Mentions have to be in the same sentence.')


def tokens_to_ngrams(tokens, ngram=(1, 1)):
    N = len(tokens)
    for root in range(N):
        for n in range(max(ngram[0] - 1, 0), min(ngram[1], N - root)):
            yield ' '.join(tokens[root: root + n + 1])


def get_left_ngrams(mention, window=3, ngram=(1, 1), lemma=False, lower=False):
    """Get the ngrams within a window to the left of a mention in a Sentence"""
    res = []
    i = mention.start_index
    tokens = mention.sentence.lemmas if lemma else mention.sentence.tokens
    for t in tokens_to_ngrams(tokens[max(0, i - window): i], ngram):
        if lower:
            t = t.lower()
        res.append(t)
    return t


def get_right_ngrams(mention, window=3, ngram=(1, 1), lemma=False, lower=False):
    """Get the ngrams within a window to the right of a mention in a Sentence"""
    res = []
    i = mention.end_index
    tokens = mention.sentence.lemmas if lemma else mention.sentence.tokens
    for t in tokens_to_ngrams(tokens[i + 1: i + 1 + window], ngram):
        if lower:
            t = t.lower()
        res.append(t)
    return t


def get_between_ngrams(mention1, mention2, ngram=(1,1), lemma=False, lower=True):
    """Return the ngrams between two mentions in the same sentence."""
    if mention1.sentence != mention2.sentence:
        return []
    dist = abs(mention1.start_index - m2.start_index)
    if mention1.start_index < mention2.start_index:
        return get_right_ngrams(mention1, window=dist - 1, ngram=ngram, lemma=lemma, lower=lower)
    else:
        return get_right_ngrams(mention2, window=dist - 1, ngram=ngram, lemma=lemma, lower=lower)