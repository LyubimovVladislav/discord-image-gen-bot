from diffusers import StableDiffusionPipeline
from PIL import Image


class Model:
    def __init__(self, *, device='cuda'):
        self.pipe = StableDiffusionPipeline.from_pretrained("Ojimi/anime-kawai-diffusion", safety_checker=None)
        self.pipe = self.pipe.to(device)
        self.i = 0

    def get_image(self, prompt: str, negative_prompt: str, width=512, height=768) -> Image:
        return \
            self.pipe(prompt, negative_prompt=negative_prompt, num_inference_steps=28, width=width,
                      height=height).images[0]

    def get_save_image(self, prompt: str, negative_prompt: str, width=512, height=768):
        filename = f'picture#{self.i}.png'
        i+=1
        self.get_image(prompt, negative_prompt, width, height).save(filename)
        return filename

