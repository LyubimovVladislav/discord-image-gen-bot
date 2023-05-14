from diffusers import StableDiffusionPipeline
from PIL import Image
from datetime import datetime


class Model:
    def __init__(self, *, device='cuda', file_format='png'):
        self.pipe = StableDiffusionPipeline.from_pretrained("Ojimi/anime-kawai-diffusion", safety_checker=None)
        self.pipe = self.pipe.to(device)
        self.file_format = file_format

    def get_image(self, prompt, negative_prompt, width=512, height=768):
        return \
            self.pipe(prompt=prompt, negative_prompt=negative_prompt, num_inference_steps=28, width=width,
                      height=height).images[0]

    def get_save_image(self, prompt, negative_prompt, width=512, height=768):
        now = datetime.now()
        filename = now.strftime("%d-%b-%Y_%H-%M-%S") + f'.{self.file_format}'
        filepath = "images/" + filename
        self.get_image(prompt, negative_prompt, width, height).save(filepath, quality=95)
        delta = datetime.now() - now
        print(f'Elapsed time: {delta.seconds// 60}m:{delta.seconds % 60}s')
        return filename, filepath
