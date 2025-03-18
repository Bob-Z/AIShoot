from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
import config
import json

with open("list.json", "r") as file:
    input_file = json.load(file)

config.read_command_line()

model = MusicGen.get_pretrained('small')
model.set_generation_params(duration=config.data['music_duration'])

wav = model.generate_unconditional(len(input_file["file_list"]))    # generates 3 unconditional audio samples
descriptions = []
for f in input_file["file_list"]:
    descriptions.append(f["prompt"])

wav = model.generate(descriptions)  # generates all sample

for idx, (one_wav, one_input) in enumerate(zip(wav, input_file["file_list"])):
    audio_write(one_input["filename"], one_wav.cpu(), model.sample_rate, strategy="loudness")
