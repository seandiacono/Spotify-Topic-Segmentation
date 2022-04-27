import torch
from transformers import BartForConditionalGeneration, BartTokenizer

class Bart:

    def __init__(self) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model = BartForConditionalGeneration.from_pretrained(
        "facebook/bart-large-xsum")
        self.tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-xsum")
        self.model = self.model.to(self.device)

    def summarize(self, segments):
        summary_segment = []
        for segment in segments:
            batch = self.tokenizer([segment], return_tensors="pt")
            output = self.model.generate(batch["input_ids"], num_beams=4)
            result = self.tokenizer.batch_decode(
                output, skip_special_tokens=True, clean_up_tokenization_spaces=False)
            obj = {result[0]: segment}
            summary_segment.append(obj)

        return summary_segment