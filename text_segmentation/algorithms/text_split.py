from sklearn.feature_extraction.text import CountVectorizer
from textsplit.tools import SimpleSentenceTokenizer
from textsplit.tools import get_penalty, get_segments
from textsplit.algorithm import split_optimal
from gensim.models import word2vec
import pandas as pd

class TextSplit:

    def __init__(self, penalty=None, segment_len=30):
        self.penalty = penalty
        self.segment_len = segment_len

    def train_model():
        sentences = word2vec.Text8Corpus("algorithms/text8/text8")
        model = word2vec.Word2Vec(sentences, vector_size=200)
        model.save("algorithms/text8/text8.model")
        
        print("Model succesfully trained and saved!")

    def segment(self, transcript):

        wc = []

        try:
            model = word2vec.Word2Vec.load("algorithms/text8/text8.model")
        except:
            print("Model needs to be trained first! Run train_model()")
            return None, None

        wrdvecs = pd.DataFrame(model.wv.vectors, index=model.wv.index_to_key)

        sentence_tokenizer = SimpleSentenceTokenizer()

        sentenced_text = sentence_tokenizer(transcript)
        vecr = CountVectorizer(vocabulary=wrdvecs.index)

        sentence_vectors = vecr.transform(sentenced_text).dot(wrdvecs)

        if not self.penalty:
            self.penalty = get_penalty([sentence_vectors], self.segment_len)
            print(f"Calculated penalty of [{self.penalty}] given segment length [{self.segment_len}]")

        optimal_segmentation = split_optimal(sentence_vectors, self.penalty)

        segments = get_segments(sentenced_text, optimal_segmentation)
        segments = [''.join(segment) for segment in segments]

        for seg in segments:
            seg = seg.split(" ")
            seg = [word for word in seg if word != "" and word != "\n\n"]
            wc.append(len(seg))

        return segments, wc

