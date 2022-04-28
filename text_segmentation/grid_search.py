import segeval
from load_transcripts import load_all_transcripts
from load_annotations import load_all_annotations
from algorithms import TextTiling, TextSplit, Baseline


transcripts_as_strings = load_all_transcripts(path="../dataset/transcripts/", as_string=True)
annotations = load_all_annotations(path=f"../dataset/annotations/", transcript_path="../dataset/transcripts")

# 1. Define the range for each variable
# TextTiling
# w = {}
# k = {}
# policy = {0, 1}

# TextSplit
# segment_len = {}

# def grid_search_text_tiling()

# min_pk = 1
# min_wd = 1

# values_pk = {}
# values_wd = {}

# for p1 in policy:
#   for w1 in w:
#       for k1 in k:

#           segmenter = text_tiling(p1, w1, k1)

#           list_pk = []
#           list_wd = []

#           for t in transcript:
#               segments = segmenter.segment(t)
#               pk = segments.error_pk()
#               wd = segments.error_wd()

#               list_pk.append(pk)
#               list_wd.append(wd)

#           average_pk = avg(list_pk)
#           average_wd = avg(list_wd)

#           if average_pk < min_pk:
#               values_pk[w] = w1
#               values_pk[k] = k1
#               values_pk[p] = p1

#           if average_wd < min_wd:
#               values_wd[w] = w1
#               values_wd[k] = k1
#               values_wd[p] = p1