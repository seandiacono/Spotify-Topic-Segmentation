import numpy as np

class Baseline:

    def __init__(self, segment_len):
        self.segment_len = segment_len # segment len is the average number of words in a segment

    def segment(self, transcript):
        words = transcript.split(" ")
        length_of_transcript = len(words) - 1

        
        cut_probability = float (1) / self.segment_len

        cuts = np.random.choice([0, 1], size=(length_of_transcript,), p=[1-cut_probability, cut_probability])

        wc = []
        current = 0

        for cut in cuts:
            if not cut:
                current += 1
            else:
                wc.append(current)
                current = 1
        wc.append(current)

        return wc