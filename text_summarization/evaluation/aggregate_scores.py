import pandas as pd
import time

# Load responses csv file
df = pd.read_csv('text_summarization/evaluation/Responses.csv', header=None)

print(df.head())

# Aggregate the responses for each model
# Collect the scores from every 4th column
# The first column is Human, the second is T5, the third is BART, and the fourth is Pegasus
human_scores = []
t5_scores = []
bart_scores = []
pegasus_scores = []
for index, row in df.iterrows():
    human_scores.append(row.tolist()[0:40:4])
    t5_scores.append(row.tolist()[1::4])
    bart_scores.append(row.tolist()[2::4])
    pegasus_scores.append(row.tolist()[3::4])

# Merge the lists into a single list
human_scores = [item for sublist in human_scores for item in sublist]
t5_scores = [item for sublist in t5_scores for item in sublist]
bart_scores = [item for sublist in bart_scores for item in sublist]
pegasus_scores = [item for sublist in pegasus_scores for item in sublist]

# Create a dataframe with the scores
df_scores = pd.DataFrame({'HUMAN': human_scores, 'T5': t5_scores, 'BART': bart_scores, 'PEGASUS': pegasus_scores})

# Save to csv
df_scores.to_csv('text_summarization/evaluation/aggregate_scores.csv', index=False)
