import json
from load_transcripts import load_all_transcripts

transcripts = load_all_transcripts(as_string=False)

with open('dataset/segments/segments_pred.json', 'r') as f:
    segments = json.load(f)

with open('dataset/segments/summaries_pred.json', 'r') as f:
    summaries = json.load(f)

segmented_summarized_episodes = {}
for episode in segments.keys():
    segment_times = []
    episode_summaries = summaries[episode]
    for segment in segments[episode]:
        # Remove /n/n and trailing whitespace
        segment = segment.strip()
        segment = segment.replace('\n\n', '')
        segment_word_list = segment.split(' ')
        for i in range(len(transcripts[episode])):
            if transcripts[episode][i]['word'] == segment_word_list[0]:
                # Join the rest of the segment
                potential_segment = transcripts[episode][i:i +
                                                         len(segment_word_list)]
                # Get just the words
                words = [x['word'] for x in potential_segment]
                # Check if the segment is the same and if it is, add the end time
                if words == segment_word_list:
                    segment_times.append(potential_segment[-1]['endTime'])

    # Join segment times and summaries
    segment_times_and_summaries = []
    for i in range(len(segment_times)):
        segment_times_and_summaries.append(
            {'segment_time': segment_times[i], 'summary': episode_summaries[i]})
    segmented_summarized_episodes[episode] = segment_times_and_summaries

# Save the segmented and summarized episodes
with open('dataset/segments/segmented_summarized_episodes.json', 'w') as f:
    json.dump(segmented_summarized_episodes, f)
