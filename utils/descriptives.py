# Script to generate average word count for our sample
import os
import json

dir = 'dataset/transcripts/'

for transcript in os.listdir(dir):
    with open(dir + transcript, 'r') as f:
        data = json.load(f)

        transcript = ''
        lengths = []
        for section in data['results']:
            try:
                transcript += section['alternatives'][0]['transcript']
                transcript += ' '
            except:
                continue
        
        transcript = transcript.split()
        lengths.append(len(transcript))

# Calculate the average word count
avg = sum(lengths) / len(lengths)
print(avg)
        
