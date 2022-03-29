from fastapi import FastAPI
from text_segmentation.load_transcripts import load_transcripts
from nltk.tokenize.texttiling import TextTilingTokenizer
import torch
from transformers import T5ForConditionalGeneration,T5Tokenizer
from fastapi.middleware.cors import CORSMiddleware
import random
from pydantic import BaseModel

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

transcripts = load_transcripts(path='spotify-podcasts-2020/podcasts-transcripts/', limit=100)

class Parameters(BaseModel):
    segmentation_type: int
    window_size: int
    block_size: int
    similarity_method: str
    smoothing_width: int
    smoothing_rounds: int
    cutoff_policy: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/segment_summary/")
def get_segment_summary(params: Parameters):
    
    print(params.segmentation_type)

    # Select Random Transcript
    transcript = random.choice(transcripts)

    # Segment Transcript
    tt = TextTilingTokenizer(w=70)
    text = tt.tokenize(transcript)

    # Load Model
    model = T5ForConditionalGeneration.from_pretrained("Michau/t5-base-en-generate-headline")
    tokenizer = T5Tokenizer.from_pretrained("Michau/t5-base-en-generate-headline")
    model = model.to(device)

    summary_segment = []

    # For Each Segment Generate Summary
    i = 0
    for segment in text:
        text_in =  "headline: " + segment

        encoding = tokenizer.encode_plus(text_in, return_tensors = "pt")
        input_ids = encoding["input_ids"].to(device)
        attention_masks = encoding["attention_mask"].to(device)

        beam_outputs = model.generate(
            input_ids = input_ids,
            attention_mask = attention_masks,
            max_length = 64,
            num_beams = 3,
            early_stopping = True,
        )

        result = tokenizer.decode(beam_outputs[0])
        obj = {result: segment}
        summary_segment.append(obj)
        i += 1
        if i >= 2:
            break

    return {'segments': summary_segment}