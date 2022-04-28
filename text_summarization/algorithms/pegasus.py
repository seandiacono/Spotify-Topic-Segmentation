import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

class Pegasus:

    def __init__(self) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model = PegasusForConditionalGeneration.from_pretrained(
        "google/pegasus-aeslc")
        self.tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-aeslc")
        self.model = self.model.to(self.device)

    def summarize(self, segments):
        summary_segment = []
        for segment in segments:
            batch = self.tokenizer([segment], truncation=True,
                            padding="longest", return_tensors="pt").to(self.device)
            output = self.model.generate(**batch)
            result = self.tokenizer.batch_decode(output, skip_special_tokens=True)
            obj = {result[0]: segment}
            summary_segment.append(obj)

        return summary_segment