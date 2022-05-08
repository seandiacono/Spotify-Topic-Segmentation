# Script to generate average word count for our sample
import os
import json
from load_transcripts import load_all_transcripts


transcripts_as_strings = load_all_transcripts(
    path="dataset/transcripts/", as_string=True)

lengths = []

for transcript in transcripts_as_strings.values():
    words = transcript.split()
    lengths.append(len(words))

# Calculate the average word count
avg = sum(lengths) / len(lengths)
print(avg)
