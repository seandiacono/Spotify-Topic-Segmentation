import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer


class T5:

    def __init__(self) -> None:
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")

        self.model = T5ForConditionalGeneration.from_pretrained(
            "Michau/t5-base-en-generate-headline")
        self.tokenizer = T5Tokenizer.from_pretrained(
            "Michau/t5-base-en-generate-headline")
        self.model = self.model.to(self.device)

    def summarize(self, segments):
        summary_segment = []

        # For Each Segment Generate Summary
        for segment in segments:
            text_in = "headline: " + segment

            encoding = self.tokenizer.encode_plus(text_in, return_tensors="pt")
            input_ids = encoding["input_ids"].to(self.device)
            attention_masks = encoding["attention_mask"].to(self.device)

            beam_outputs = self.model.generate(
                input_ids=input_ids,
                attention_mask=attention_masks,
                max_length=25,
                num_beams=3,
                early_stopping=True,
            )

            result = self.tokenizer.decode(beam_outputs[0])
            obj = {result: segment}
            summary_segment.append(obj)

        return summary_segment
