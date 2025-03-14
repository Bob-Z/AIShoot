import os
import time
from diffusers import StableDiffusionPipeline
import torch

print("Generating initial images")

# Directory to save generated images
output_dir = "generated_image"
os.makedirs(output_dir, exist_ok=True)

# Load the pipeline
model_id = "CompVis/stable-diffusion-v1-4"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

# Function to generate a new image with an alpha channel
def generate_sprite(prompt, filename):
    image = pipe(prompt).images[0]
    image = image.convert("RGBA")  # Convert to RGBA to include alpha channel
    image.save(filename)
    print(f"Generated new image with alpha channel: {filename}")  # Debugging information

# Generate initial sprites if they don't exist
if not os.path.exists(os.path.join(output_dir, "player.png")):
    generate_sprite("A futuristic spaceship", os.path.join(output_dir, "player.png"))
if not os.path.exists(os.path.join(output_dir, "enemy.png")):
    generate_sprite("An alien spaceship", os.path.join(output_dir, "enemy.png"))
if not os.path.exists(os.path.join(output_dir, "bullet.png")):
    generate_sprite("A laser beam", os.path.join(output_dir, "bullet.png"))
if not os.path.exists(os.path.join(output_dir, "background.png")):
    generate_sprite("A space background", os.path.join(output_dir, "background.png"))

# Create a flag file to indicate that initial images are generated
with open(os.path.join(output_dir, "initial_images_generated.flag"), "w") as f:
    f.write("Initial images generated")

# Generate new enemy images in batches
image_counter = 0
batch_size = 5
while True:
    for _ in range(batch_size):
        image_counter += 1
        filename = os.path.join(output_dir, f"new_enemy_{image_counter}.png")
        generate_sprite("A new alien spaceship", filename)
    time.sleep(2)  # Wait for 2 seconds before generating a new batch

