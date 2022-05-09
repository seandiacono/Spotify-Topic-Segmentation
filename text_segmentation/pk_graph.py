from load_transcripts import load_all_transcripts
from load_annotations import load_all_annotations
from algorithms import TextSplit
import segeval
import pandas as pd
import matplotlib.pyplot as plt

transcripts_as_strings = load_all_transcripts(
    path="../dataset/transcripts/", as_string=True)
annotations = load_all_annotations(
    path=f"../dataset/annotations/", transcript_path="../dataset/transcripts")

df = pd.read_csv("../text_summarization/evaluation/averages.csv")

wc_sum = 0
wc_len = 0

for id in annotations:
    wc_sum += sum(annotations[id])
    wc_len += len(annotations[id])

avg_segment_wc_len = wc_sum / wc_len

text_split_segmenter = TextSplit(segment_len=10)

pk_scores = []
wd_scores = []
for key in df['Podcast_Id']:
    # print(key)
    wc_truth = annotations[key]
    transcript = transcripts_as_strings[key]

    _, wc_split = text_split_segmenter.segment(transcript)

    if sum(wc_truth) != sum(wc_split):
        diff = sum(wc_truth) - sum(wc_split)
        wc_split[-1] = wc_split[-1] + diff

    pk_scores.append(segeval.pk(wc_truth, wc_split))
    wd_scores.append(segeval.window_diff(wc_truth, wc_split))

# Convert pk and wd scores to floats
pk_scores = [float(x) for x in pk_scores]
wd_scores = [float(x) for x in wd_scores]
print(pk_scores)
print(wd_scores)

# # Plot the pk scores on the x axis and the relevancy scores on the y axis
# human_x, human_y = zip(*sorted(zip(pk_scores, df['HUMAN'])))
# t5_x, t5_y = zip(*sorted(zip(pk_scores, df['T5'])))
# bart_x, bart_y = zip(*sorted(zip(pk_scores, df['BART'])))
# pegasus_x, pegasus_y = zip(*sorted(zip(pk_scores, df['PEGASUS'])))

# plt.plot(human_x, human_y, label="Human")
# plt.plot(t5_x, t5_y, label="T5")
# plt.plot(bart_x, bart_y, label="BART")
# plt.plot(pegasus_x, pegasus_y, label="Pegasus")
# plt.legend()
# plt.show()
