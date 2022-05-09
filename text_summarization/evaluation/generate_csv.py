import pandas as pd
from transformers import BART_PRETRAINED_MODEL_ARCHIVE_LIST

# Load responses csv file
df = pd.read_csv('text_summarization/evaluation/responses.csv')

# Iterate over each
segments = []
no_of_rows = 0
for index, row in df.iterrows():
    # Get first 4 values from row
    if len(segments) == 0:
        segments.append(row[0:4])
        segments.append(row[4:8])
        segments.append(row[8:12])
        segments.append(row[12:16])
        segments.append(row[16:20])
        segments.append(row[20:24])
        segments.append(row[24:28])
        segments.append(row[28:32])
        segments.append(row[32:36])
        segments.append(row[36:40])
    else:
        segments[0] = [a + b for a, b in zip(segments[0], row[0:4])]
        segments[1] = [a + b for a, b in zip(segments[1], row[4:8])]
        segments[2] = [a + b for a, b in zip(segments[2], row[8:12])]
        segments[3] = [a + b for a, b in zip(segments[3], row[12:16])]
        segments[4] = [a + b for a, b in zip(segments[4], row[16:20])]
        segments[5] = [a + b for a, b in zip(segments[5], row[20:24])]
        segments[6] = [a + b for a, b in zip(segments[6], row[24:28])]
        segments[7] = [a + b for a, b in zip(segments[7], row[28:32])]
        segments[8] = [a + b for a, b in zip(segments[8], row[32:36])]
        segments[9] = [a + b for a, b in zip(segments[9], row[36:40])]

    no_of_rows += 1

# Convert sums to averages
for segment in segments:
    for i in range(len(segment)):
        segment[i] = segment[i] / no_of_rows

# Convert to dataframe where each row is a segment
df_segments = pd.DataFrame(segments)
df_segments.columns = ['HUMAN', 'T5', 'BART', 'PEGASUS']

# Save to csv
df_segments.to_csv('text_summarization/evaluation/averages.csv')