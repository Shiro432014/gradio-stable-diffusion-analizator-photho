import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"

# Важно: добавляем use_fast=True
processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-large",
    use_fast=True
)

model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-large"
).to(device)


def generate_caption(image: Image.Image) -> str:
    image = image.convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(device)
    out = model.generate(**inputs, max_length=60)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption.strip().capitalize()
