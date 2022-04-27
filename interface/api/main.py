from fastapi import FastAPI
from text_segmentation.load_transcripts_old import load_transcripts
from nltk.tokenize.texttiling import TextTilingTokenizer
from nltk.tokenize import sent_tokenize, word_tokenize
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
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
    segmentation_type: int
    podcast_index: int
    num_segments: int
    window_size: Optional[int] = None
    block_size: Optional[int] = None
    smoothing_width: Optional[int] = None
    smoothing_rounds: Optional[int] = None
    cutoff_policy: Optional[str] = None
    split_penalty: Optional[float] = None



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
    print(sentenced_text)
    print(segmented_text)

    # For each segment join the sentences back together
    segmented_text = [''.join(segment) for segment in segmented_text]

    return segmented_text


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/segment_summary/")
def get_segment_summary(params: Parameters):

    # Select Random Transcript
    # transcript = random.choice(transcripts)

    transcript = transcripts[params.podcast_index]

    if params.segmentation_type == 1:
        # Segment Transcript
        tt = TextTilingTokenizer(w=params.window_size, k=params.block_size,
                                 smoothing_width=params.smoothing_width, smoothing_rounds=params.smoothing_rounds, cutoff_policy=params.cutoff_policy)
        text = tt.tokenize(transcript)
    else:
        text = textsplit(transcript, params.split_penalty)

    # Load Model
    model = T5ForConditionalGeneration.from_pretrained(
        "Michau/t5-base-en-generate-headline")
    tokenizer = T5Tokenizer.from_pretrained(
        "Michau/t5-base-en-generate-headline")
    model = model.to(device)

    summary_segment = []

    # For Each Segment Generate Summary
    i = 0
    for segment in text:
        text_in = "headline: " + segment

        encoding = tokenizer.encode_plus(text_in, return_tensors="pt")
        input_ids = encoding["input_ids"].to(device)
        attention_masks = encoding["attention_mask"].to(device)

        beam_outputs = model.generate(
            input_ids=input_ids,
            attention_mask=attention_masks,
            max_length=10,
            num_beams=3,
            early_stopping=True,
        )

        result = tokenizer.decode(beam_outputs[0])
        obj = {result: segment}
        summary_segment.append(obj)
        i += 1
        if i >= params.num_segments:
            break

    return {'segments': summary_segment}
