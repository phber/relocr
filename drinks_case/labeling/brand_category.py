import re
from relocr.utils.visual import is_vert_aligned, is_horz_aligned, get_aligned_tokens


ABSTAIN = 0
FALSE = 1
TRUE = 2


def IS_ONLY_CAT_ON_PAGE(document, brand, cat):
    page = document.get_page(cat.page)
    return TRUE if len(page.get_mentions('category')) == 1 else FALSE


def FIRST_PAGE_CONTAINS_CAT(document, brand, cat):
    first_page = document.get_page(1)
    for mention in first_page.get_mentions('category'):
        if mention.name == cat.name:
            return TRUE
    return ABSTAIN


def BRAND_CAT_VERT_ALIGNED(document, brand, cat):
    return TRUE if is_vert_aligned(brand.sentence, cat.sentence) else FALSE


def BRAND_CAT_HORZ_ALIGNED(document, brand, cat):
    return TRUE if is_horz_aligned(brand.sentence, cat.sentence) else ABSTAIN


def CONTAINS_BRAND_VERT(document, brand, cat):
    pg = document.get_page(brand.page)
    for toks in get_aligned_tokens(brand.sentence, pg):
        if brand.lower() in toks.lower():
            return TRUE
    return ABSTAIN


def SENT_CONTAINS_CATEGORY(document, brand, cat):
    return TRUE if 'category' in cat.sentence.lemmas else ABSTAIN


def SENT_CONTAINS_CONTAINS(document, brand, cat):
    return FALSE if 'contain' in cat.sentence.text else ABSTAIN


def PAGE_CONTAINS_FLAVOURS(document, brand, cat):
    page = document.get_page(cat.page)
    for sent in page.get_sentences('text'):
        if ('flavour' in sent) or ('flavour' in sent):
            return FALSE
    return ABSTAIN


def SAME_SENTENCE(document, brand, cat):
    return TRUE if (brand.sentence == cat.sentence) else ABSTAIN
