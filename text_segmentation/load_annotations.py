# A script to load annotations, returning them as a list of word counts

from load_transcripts import load_transcript
import pandas as pd
import os

ftr = [60,1]

# A function that returns all annotations in the format of {episode_id: list_of_word_counts, ...}
def load_all_annotations(path="dataset/annotations", transcript_path= "dataset/transcripts"):

    all_annotations = {}

    for file in os.listdir(path):
        episode_id, annotations = load_annotations(f"{path}/{file}", transcript_path)

        all_annotations[episode_id] = annotations

    return all_annotations

# A function that loads a specific annotation in the format of (episode_id, list_of_word_counts)
def load_annotations(path, transcript_path = "dataset/transcripts"):

    episode_id = path.split("- ")[1].split(".")[0]

    df = pd.read_csv(path)  

    annotations_seconds =  df["Time"].astype(str).map(convert_to_seconds).tolist()

    annotations_wc = convert_to_wc(episode_id, annotations_seconds, transcript_path)

    return episode_id, annotations_wc

# A function that converts a time string (such as 45.58) into its second equivalent (2758)
def convert_to_seconds(timestr):
    m, s = timestr.split(".")

    if len(s) == 1: s += "0"

    return int(m) * 60 + int(s)

# A function that converts annotation seconds to annotation word counts 
def convert_to_wc(episode_id, annotations_seconds, transcript_path):
    transcript = load_transcript(f"{transcript_path}/{episode_id}.json", as_string=False)

    wc = 0
    index_annotations = 0
    annotations_wc = []

    for index_transcript, word in enumerate(transcript):

        wc += 1
        endTime = float(word["endTime"][:-1])

        if endTime > annotations_seconds[index_annotations]:
            annotations_wc.append(wc)
            wc = 0
            index_annotations += 1

            # In reality, the last annotated segment end is not taken in consideration
            if index_annotations == len(annotations_seconds) - 1:
                 wc += len(transcript) - index_transcript - 1
                 annotations_wc.append(wc)
                 break

    return annotations_wc