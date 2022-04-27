import os
import json

def load_all_transcripts(path="dataset/transcripts", as_string=True):
    transcripts = {}

    for file in os.listdir(path):
        episode_id = file.split(".")[0]
        transcripts[episode_id] = load_transcript(f"{path}/{file}", as_string)

    return transcripts

def load_transcript(path, as_string=True):

    if as_string: transcript = ""
    else: transcript = []

    
    with open(path, 'r') as f:
        data = json.load(f)
       
        for section in data['results']:

            try:

                words = section['alternatives'][0]['words']

                # Ignore take speaker tag alternatives
                if 'speakerTag' in words[0]:
                    break

                if as_string:
                    for word in words:
                        transcript += word["word"] + " "
                    transcript += "\n\n"
                else:
                    transcript.extend(section['alternatives'][0]['words'])
            except:
                continue

    return transcript
    