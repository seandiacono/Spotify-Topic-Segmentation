from load_transcripts import load_all_transcripts
from algorithms import TextSplit
import json

# TextSplit to segment the sample transcript

transcripts_as_strings = load_all_transcripts(
    path="../dataset/transcripts/", as_string=True)

segment_dict = {}

for episode_id in transcripts_as_strings.keys():
    segmenter = TextSplit(segment_len=10)
    segments_pred, _ = segmenter.segment(transcripts_as_strings[episode_id])

    segment_dict[episode_id] = segments_pred

# Save to json 
with open("../dataset/segments/segments_pred.json", "w") as f:
    json.dump(segment_dict, f)