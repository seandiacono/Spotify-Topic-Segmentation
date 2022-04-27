# A script to handle loading all transcripts from the spotify podcasts data

import os
import json
import tqdm

# Function to load all transcripts from the spotify podcasts data and return a list of all transcripts


def load_transcripts(path='spotify-podcasts-2020/podcasts-transcripts/', limit=100):
    transcripts = []
    i = 0
    pbar = tqdm.tqdm(total=limit)

    # Iterate through all directories in the spotify podcasts data
    for dir in os.listdir(path):
        # Iterate through all subdirectories
        for subdir in os.listdir(path + dir):
            # Iterate through all show directories
            for show in os.listdir(path + dir + '/' + subdir):
                # Iterate through all transcript files
                for transcript in os.listdir(path + dir + '/' + subdir + '/' + show):
                    # Open the transcript file
                    with open(path + dir + '/' + subdir + '/' + show + '/' + transcript, 'r') as f:
                        data = json.load(f)
                        # Join all the transcriptions into one string
                        transcript = ''
                        for section in data['results']:
                            try:
                                transcript += section['alternatives'][0]['transcript']
                                # Add paragraph breaks
                                transcript += '\n\n'
                            except:
                                continue
                        # Add the transcript to the list of transcripts
                        transcripts.append(transcript)
                        i += 1
                        pbar.update(1)
                        # Limit the number of transcripts to load
                        if i >= limit:
                            return transcripts

    return transcripts