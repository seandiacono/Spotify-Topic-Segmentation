import json
from algorithms.t5 import T5
from algorithms.pegasus import Pegasus
from algorithms.bart import Bart

# Load the segment json
with open("../dataset/segments/segments_pred_sampled.json", "r") as f:
    segments_pred = json.load(f)

t5 = T5()
print("T5 initalized")
bart = Bart()
print("BART initalized")
pegasus = Pegasus()
print("Pegasus initalized")

summarized_segments = {}

i = 1
# For each segment generate summaries using all 3 models
for episode_id in segments_pred.keys():
    summaries = []
    t5_summary = t5.summarize([segments_pred[episode_id]])
    summaries.append(t5_summary)
    bart_summary = bart.summarize([segments_pred[episode_id]])
    summaries.append(bart_summary)
    pegasus_summary = pegasus.summarize([segments_pred[episode_id]])
    summaries.append(pegasus_summary)
    print(f"Episode {i}")
    print(f"T5: {t5_summary}")
    print(f"BART: {bart_summary}")
    print(f"Pegasus: {pegasus_summary}")

    i += 1
    summarized_segments[episode_id] = summaries

# Save the summarized segments
with open("../dataset/segments/summarized_segments.json", "w") as f:
    json.dump(summarized_segments, f)
