import torchaudio
from audiocraft.models import AudioGen
from audiocraft.data.audio import audio_write
import os

print("Generating sounds")

output_dir = "generated_sound"
os.makedirs(output_dir, exist_ok=True)

model = AudioGen.get_pretrained('facebook/audiogen-medium')
model.set_generation_params(duration=3)  # generate 3 seconds.

print("Generating player's weapon sound")
descriptions = ['strange weapon single shot']
wav = model.generate(descriptions)  # generates 1 samples.
audio_write(f'{output_dir}/shoot', wav[0].cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)

print("Generating enemies' explosion sound")
descriptions = ['brutal explosion', 'small explosion', 'fast explosion', 'short explosion', 'tiny explosion']
wav = model.generate(descriptions)  # generates 5 samples.
for idx, one_wav in enumerate(wav):
    # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
    audio_write(f'{output_dir}/hit{idx}', one_wav.cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)
