from relocr.utils.visual import *
import itertools

class AlignedLemmasFeature(AbstractFeature):
    def apply(self, mention1, mention2, features):
        


class AlignedFeature(AbstractFeature):
    def apply(self, mention1, mention2, features):
        if is_horz_aligned(mention1, mention2):
            features.append("HORZ_ALIGNED")
        if is_vert_aligned(mention1, mention2):
            features.append("VERT_ALIGNED")
        if is_vert_aligned_left(mention1, mention2):
            features.append("VERT_ALIGNED_LEFT")
        if is_vert_aligned_right(mention1, mention2):
            features.append("VERT_ALIGNED_RIGHT")
        if is_vert_aligned_center(mention1, mention2):
            features.append("VERT_ALIGNED_CENTER")
