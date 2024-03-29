from nltk.tokenize.texttiling import TextTilingTokenizer

class TextTiling:

    def __init__(self, w=20, k=10, policy=0):
        # 0 policy is liberal, 1 is conservative
        self.segmenter = TextTilingTokenizer(w, k, cutoff_policy=policy)

    def segment(self, transcript):
        segments = self.segmenter.tokenize(transcript)
        wc = []

        for seg in segments:
            seg = seg.split(" ")
            seg = [word for word in seg if word != "" and word != "\n\n"]
            wc.append(len(seg))

        return segments, wc

