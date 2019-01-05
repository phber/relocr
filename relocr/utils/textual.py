def get_between_tokens(m1, m2):
    """Return the tokens between two mentions"""
    if m1.sentence != m2.sentence:
        raise ValueError('Mentions have to be in the same sentence.')
    

def get_left_ngrams(sentence, mention):
    return

def get_right_ngrams(sentence, mention):
    return
