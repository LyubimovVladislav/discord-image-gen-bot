from diffusers import StableDiffusionPipeline
from PIL import Image
from datetime import datetime
from torch import float16, float32


class Model:
    def __init__(self, *, repository: str, half_precision: bool = False, quality=95, device='cuda', file_format='png'):
        self.quality = quality
        self.torch_dtype = float16 if half_precision else float32
        self.pipe = StableDiffusionPipeline.from_pretrained(repository,
                                                            safety_checker=None, torch_dtype=self.torch_dtype)
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
        self.get_image(prompt, negative_prompt, width, height).save(filepath, quality=self.quality)
        delta = datetime.now() - now
        print(f'Elapsed time: {delta.seconds // 60}m:{delta.seconds % 60}s')
        return filename, filepath
