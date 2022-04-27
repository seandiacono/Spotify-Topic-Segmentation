from os import truncate
from fastapi import FastAPI
from text_segmentation.load_transcripts import load_transcripts
from nltk.tokenize.texttiling import TextTilingTokenizer
from nltk.tokenize import sent_tokenize, word_tokenize
from fastapi.middleware.cors import CORSMiddleware
import random
from pydantic import BaseModel
from sklearn.feature_extraction.text import CountVectorizer
from gensim.models import word2vec
import pandas as pd
from textsplit.tools import SimpleSentenceTokenizer
from textsplit.tools import get_penalty, get_segments
from textsplit.algorithm import split_optimal
from typing import Optional
from text_summarization.algorithms.bart import Bart
from text_summarization.algorithms.pegasus import Pegasus
from text_summarization.algorithms.t5 import T5

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

transcripts = load_transcripts(
    path='spotify-podcasts-2020/podcasts-transcripts/', limit=100)


class Parameters(BaseModel):
    podcast_index: int
    window_size: Optional[int] = None
    block_size: Optional[int] = None
    smoothing_width: Optional[int] = None
    smoothing_rounds: Optional[int] = None
    cutoff_policy: Optional[str] = None
    split_penalty: Optional[float] = None


class Segmentation(BaseModel):
    segments: list = []
    num_segments: int


def textsplit(transcript, split_penalty):

    transcript = transcript.lower()
    # Split the transcript into sentences of words
    sentences = sent_tokenize(transcript)
    # Split each sentence into words and lowercase them
    words = [word_tokenize(sentence) for sentence in sentences]

    # Train a word2vec model
    model = word2vec.Word2Vec(words, vector_size=100, window=3, min_count=1,)

    wrdvecs = pd.DataFrame(model.wv.vectors, index=model.wv.index_to_key)

    sentence_tokenizer = SimpleSentenceTokenizer()

    sentenced_text = sentence_tokenizer(transcript)
    vecr = CountVectorizer(vocabulary=wrdvecs.index)

    sentence_vectors = vecr.transform(sentenced_text).dot(wrdvecs)

    # penalty = get_penalty([sentence_vectors], segment_len)
    penalty = split_penalty

    optimal_segmentation = split_optimal(sentence_vectors, penalty)
    segmented_text = get_segments(sentenced_text, optimal_segmentation)

    # For each segment join the sentences back together
    segmented_text = [''.join(segment) for segment in segmented_text]

    return segmented_text


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/text_tiling")
def text_tiling(params: Parameters):
    transcript = transcripts[params.podcast_index]

    # Segment Transcript
    tt = TextTilingTokenizer(w=params.window_size, k=params.block_size,
                             smoothing_width=params.smoothing_width, smoothing_rounds=params.smoothing_rounds, cutoff_policy=params.cutoff_policy)

    text = tt.tokenize(transcript)

    return text


@app.post("/text_split")
def text_split(params: Parameters):
    transcript = transcripts[params.podcast_index]

    # Segment Transcript
    segmented_text = textsplit(transcript, params.split_penalty)

    return segmented_text


@app.post("/t5_summarization")
def t5_summarization(segmentation: Segmentation):
    # Summarize the segmented transcript
    t5 = T5()

    summary = t5.summarize(segmentation.segments)

    return {'segments': summary}


@app.post("/pegasus_summarization")
def pegasus_summarization(segmentation: Segmentation):
    # Summarize the segmented transcript
    pegasus = Pegasus()

    summary = pegasus.summarize(segmentation.segments)

    return {'segments': summary}


@app.post("/bart_summarization")
def bart_summarization(segmentation: Segmentation):
    # Summarize the segmented transcript
    bart = Bart()

    summary = bart.summarize(segmentation.segments)

    return {'segments': summary}
