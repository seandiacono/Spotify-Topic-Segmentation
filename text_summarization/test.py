from algorithms.t5 import T5
from algorithms.pegasus import Pegasus
from algorithms.bart import Bart


text = 'I think it happened high up on a hillside in Switzerland high on a hill and a cow drop some milk into a field in may be its own hoof print and then I think it mixed with all the stuff in the dirt and \n\nthe grass and a baked in the Sun and then I think a farmer walked by and said mmm, that looks interesting and then ate it. \n\n'
desciption = "When did someone first see a cheese curd and think, Yeah, I'm going to eat that? ELT traces the delicious and X-rated history of cheese. Plus, a professional processed cheese maker on how to make the most of the dairy aisle. Guests: cheese biochemist and historian Paul Kindstedt; processed cheese expert Lloyd Metzger; and cicada killer wasp biologist Chuck Holliday. Thanks to callers Kurt and Judi.  Have a question that needs answering? Call the ELT Help Line #(833) RING ELT. To find a list of our sponsors and show-related promo codes, go to gimlet.media/OurAdvertisers."

segment = text + " " + desciption

t5 = T5()
print("T5 initalized")
bart = Bart()
print("BART initalized")
pegasus = Pegasus()
print("Pegasus initalized")

t5_summary = t5.summarize([segment])
bart_summary = bart.summarize([segment])
pegasus_summary = pegasus.summarize([segment])
print(f"T5: {t5_summary}")
print(f"BART: {bart_summary}")
print(f"Pegasus: {pegasus_summary}")
