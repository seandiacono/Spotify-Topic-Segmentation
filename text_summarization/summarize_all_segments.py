import json
from algorithms.t5 import T5
from algorithms.pegasus import Pegasus
from algorithms.bart import Bart

# Load the segment json
with open("../dataset/segments/segments_pred.json", "r") as f:
    segments_pred = json.load(f)

t5 = T5()
print("T5 initalized")

summarized_segments = {}

i = 1
# For each segment generate summaries using all 3 models
for episode_id in segments_pred.keys():
    summaries = []
    for segment in segments_pred[episode_id]:
        t5_summary = t5.summarize([segment])
        t5_summary = list(t5_summary[0].keys())[0]
        # Remove <pad> and </s>
        t5_summary = t5_summary.replace("<pad>", "")
        t5_summary = t5_summary.replace("</s>", "")
        summaries.append(t5_summary)
        print(t5_summary)
    i += 1
    summarized_segments[episode_id] = summaries

# Save the summarized segments
with open("../dataset/segments/summarized_all_segments.json", "w") as f:
    json.dump(summarized_segments, f)
