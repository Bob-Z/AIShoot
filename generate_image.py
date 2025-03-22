import os
from diffusers import StableDiffusionPipeline
import torch
import json

with open("list.json", "r") as file:
    input_file = json.load(file)

# Load the pipeline
model_id = "CompVis/stable-diffusion-v1-4"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

# Function to generate a new image
for d in input_file["file_list"]:
    print(f'Generating image {d["filename"]} with prompt: {d["prompt"]}')
    image = pipe(prompt=d["prompt"], height=512, width=512).images[0]
    image.save("tmp.png")
    os.rename("tmp.png", d["filename"])  # Avoid game engine to read a file while it is not entirely written on the disk

