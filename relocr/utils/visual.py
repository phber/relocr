from itertools import groupby


def splitWithIndices(s, c=' '):
    # Split string and store indices
    p = 0
    for k, g in groupby(s, lambda x: x == c):
        q = p + sum(1 for i in g)
        if not k:
            yield p, q 
        p = q


def is_horz_aligned(e1, e2):
    """ Returns true if the vertical center point of either span is within the vertical range of the other """
    e1_top = e1.top + 1.5
    e2_top = e2.top + 1.5
    e1_bottom = e1.bottom - 1.5
    e2_bottom = e2.bottom - 1.5
    return not (e1_top > e2_bottom or e2_top > e1_bottom)


def is_vert_aligned(e1, e2):
    """ Returns true if the hors center point of either span is within the vertical range of the other """
    e1_left = e1.left + 1.5
    e2_left = e2.left + 1.5
    e1_right = e1.right - 1.5
    e2_right = e2.right - 1.5
    return not (e1_left > e2_right or e2_left > e1_right)


def is_vert_aligned_center(e1, e2):
    """ Returns true if the center of both boxes is within 5 pts """
    return abs(((e1.right + e1.left) / 2.0) - ((e2.right + e2.left) / 2.0)) <= 5


def is_vert_aligned_right(e1, e2):
    """ Returns true if the right boundary of both boxes is within 2 pts """
    return abs(e1.right - e2.right) <= 2


def is_vert_aligned_left(e1, e2):
    """ Returns true if the left boundary of both boxes is within 2 pts """
    return abs(e1.left - e2.left) <= 2


def is_below(e1, e2):
    """ Returns true if e2 is below e1 """
    return True if e1.top > e2.top else False


def is_right_of(e1, e2):
    """ Returns true if e2 is right of e1 """
    return True if e2.right > e1.right else False


def get_page_vert_percentile(mention, page_height):
    """ Returns a value 0 - 1 from bottom (i.e bottom of the page)"""
    return 1.0 * mention.top / page_height


def get_page_horz_percentile(mention, page_width):
    """ Returns a value 0 - 1 from left (i.e left of the page)"""
    return 1.0 * mention.left / page_width


def get_aligned_tokens(sentence, page, max_len=5):
    """ Returns dict of aligned sentences"""
    res = {'above': [], 'below': [], 'left': [], 'right': []}
    box0 = sentence.textbox
    for box in page.boxes:
        if box0 == box:
            continue
        if len(box.text.split()) > max_len:
            continue
        if is_horz_aligned(box, box0):
            if box.right > box0.right:
                res['right'].append(box.sentences[0])
            else:
                res['left'].append(box.sentences[0])
        elif is_vert_aligned(box, box0):
            if box.bottom > box0.bottom:
                res['above'].append(box.sentences[0])
            else:
                res['below'].append(box.sentences[0])
    return res
