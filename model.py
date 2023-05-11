from diffusers import StableDiffusionPipeline
from PIL import Image


class Model:
    def __init__(self, *, device='cuda'):
        self.pipe = StableDiffusionPipeline.from_pretrained("Ojimi/anime-kawai-diffusion", safety_checker=None)
        self.pipe = self.pipe.to(device)
        self.i = 0
        self.generates = False

    def get_image(self, prompt, negative_prompt, width=512, height=768):
        return \
            self.pipe(prompt=prompt, negative_prompt=negative_prompt, num_inference_steps=28, width=width,
                      height=height).images[0]

    def get_save_image(self, prompt, negative_prompt, width=512, height=768):
        if not self.generates:
            return None
        self.generates = True
        filename = f'picture_{self.i}.png'
        self.i += 1
        self.get_image(prompt, negative_prompt, width, height).save(filename)
        self.generates = False
        return filename

    async def manual_reset(self):
        self.generates = False
