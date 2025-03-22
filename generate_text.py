import torch
from transformers import pipeline
import config
import json
import os

with open("list.json", "r") as file:
    input_file = json.load(file)

config.read_command_line()

pipe = pipeline("text-generation", model="HuggingFaceH4/zephyr-7b-beta", torch_dtype=torch.bfloat16, device_map="auto")

for d in input_file["file_list"]:
    print(f'Generating taunt in {d["filename"]} with {d["prompt"]}')
    prompt = pipe.tokenizer.apply_chat_template(d["prompt"], tokenize=False, add_generation_prompt=True)
    outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    with open("tmp.txt", "w") as text_file:
        text_file.write(outputs[0]["generated_text"].splitlines()[-1])
    os.rename("tmp.txt", d["filename"])  # Avoid game engine to read a file while it is not entirely written on the disk