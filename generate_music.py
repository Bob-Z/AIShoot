import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
import os
import config

config.read_command_line()

model = MusicGen.get_pretrained('small')
model.set_generation_params(duration=config.data['music_duration'])

wav = model.generate_unconditional(3)    # generates 3 unconditional audio samples
#descriptions = ['shooting game rock music', 'shooting game electronic music', 'shooting game rap music', 'shooting game classical music','shooting game 8 bits music']
descriptions = ['shooting game rock music', 'shooting game orchestral music','shooting game 8 bits music']

wav = model.generate(descriptions)  # generates 5 samples.

for idx, one_wav in enumerate(wav):
    filename = os.path.join("generated_music", f"{idx}")
    # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
    audio_write(filename, one_wav.cpu(), model.sample_rate, strategy="loudness")
