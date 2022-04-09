from os import truncate
from fastapi import FastAPI
from text_segmentation.load_transcripts import load_transcripts
from nltk.tokenize.texttiling import TextTilingTokenizer
from nltk.tokenize import sent_tokenize, word_tokenize
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer, PegasusForConditionalGeneration, PegasusTokenizer, BartForConditionalGeneration, BartTokenizer
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

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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


# TODO: 1. Break down api endpoint into segmentation and summarization
# TODO: 2. Add api endpoints for BART and Pegasus
# TODO: 3. Move segmentation type choice to client side

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
    # Load Model
    model = T5ForConditionalGeneration.from_pretrained(
        "Michau/t5-base-en-generate-headline")
    tokenizer = T5Tokenizer.from_pretrained(
        "Michau/t5-base-en-generate-headline")
    model = model.to(device)

    summary_segment = []

    # For Each Segment Generate Summary
    i = 0
    for segment in segmentation.segments:
        text_in = "headline: " + segment

        encoding = tokenizer.encode_plus(text_in, return_tensors="pt")
        input_ids = encoding["input_ids"].to(device)
        attention_masks = encoding["attention_mask"].to(device)

        beam_outputs = model.generate(
            input_ids=input_ids,
            attention_mask=attention_masks,
            max_length=15,
            num_beams=3,
            early_stopping=True,
        )

        result = tokenizer.decode(beam_outputs[0])
        obj = {result: segment}
        summary_segment.append(obj)
        i += 1
        if i >= segmentation.num_segments:
            break

    return {'segments': summary_segment}


@app.post("/pegasus_summarization")
def pegasus_summarization(segmentation: Segmentation):
    model = PegasusForConditionalGeneration.from_pretrained(
        "google/pegasus-aeslc")
    tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-aeslc")
    model = model.to(device)

    summary_segment = []
    i = 0
    for segment in segmentation.segments:
        batch = tokenizer([segment], truncation=True,
                          padding="longest", return_tensors="pt").to(device)
        output = model.generate(**batch)
        result = tokenizer.batch_decode(output, skip_special_tokens=True)
        obj = {result[0]: segment}
        summary_segment.append(obj)
        i += 1
        if i >= segmentation.num_segments:
            break

    return {'segments': summary_segment}


@app.post("/bart_summarization")
def bart_summarization(segmentation: Segmentation):
    model = BartForConditionalGeneration.from_pretrained(
        "facebook/bart-large-xsum")
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-xsum")
    model = model.to(device)

    summary_segment = []
    i = 0
    for segment in segmentation.segments:
        batch = tokenizer([segment], return_tensors="pt")
        output = model.generate(batch["input_ids"], num_beams=4)
        result = tokenizer.batch_decode(
            output, skip_special_tokens=True, clean_up_tokenization_spaces=False)
        obj = {result[0]: segment}
        summary_segment.append(obj)
        i += 1
        if i >= segmentation.num_segments:
            break

    return {'segments': summary_segment}
