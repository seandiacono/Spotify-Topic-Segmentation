import json
import random

# Load segment json
with open("../dataset/segments/segments_pred.json", "r") as f:
    segments_pred = json.load(f)

sampled_segments = {}

# Get one random segment from each episode
for episode_id in segments_pred.keys():
    sampled_segments[episode_id] = random.choice(segments_pred[episode_id])

# Save sampled segments
with open("../dataset/segments/segments_pred_sampled.json", "w") as f:
    json.dump(sampled_segments, f)