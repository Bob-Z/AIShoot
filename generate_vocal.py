import scipy
from transformers import AutoProcessor, BarkModel
import json
import os
import config

with open("list.json", "r") as file:
    input_file = json.load(file)

config.read_command_line()

processor = AutoProcessor.from_pretrained("suno/bark")
model = BarkModel.from_pretrained("suno/bark")

for f in input_file["file_list"]:
    #inputs = processor(""" Your puny human defense systems will not prevent the inevitable destruction of your planet. Prepare for annihilation. """, voice_preset="v2/en_speaker_5")
    inputs = processor(f["text"], voice_preset=f["voice"])
    audio_array = model.generate(**inputs)
    audio_array = audio_array.cpu().numpy().squeeze()
    sample_rate = model.generation_config.sample_rate
    scipy.io.wavfile.write("tmp.wav",rate=sample_rate, data=audio_array)
    os.rename("tmp.wav",
              f["filename"])  # Avoid game engine to read a file while it is not entirely written on the disk