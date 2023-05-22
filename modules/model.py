from datetime import datetime

from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler, EulerAncestralDiscreteScheduler, \
    KDPM2DiscreteScheduler, UniPCMultistepScheduler, DDPMScheduler, HeunDiscreteScheduler, \
    KDPM2AncestralDiscreteScheduler, DEISMultistepScheduler, PNDMScheduler, DDIMScheduler, \
    DPMSolverSinglestepScheduler, LMSDiscreteScheduler, EulerDiscreteScheduler
import torch
from transformers import CLIPTextModel

from decorators.timer import timer
from modules.config import Config
from modules.parser import Parser


class Model:
    # noinspection SpellCheckingInspection
    def __init__(self, *, repository: str, half_precision: bool = False, quality=95, device='cuda', file_format='png'):
        self.quality = quality
        self.torch_dtype = torch.float16 if half_precision else torch.float32
        self.repository = repository
        self.pipe = StableDiffusionPipeline.from_pretrained(repository,
                                                            safety_checker=None, torch_dtype=self.torch_dtype)
        self.pipe = self.pipe.to(device)
        self.file_format = file_format
        name = repository.split('/')
        self.name = name[-1] if name else ''

    def _get_image(self, prompt, negative_prompt, width, height, scale, steps, generator):
        return self.pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=steps,
            width=width,
            height=height,
            guidance_scale=scale,
            generator=generator
        ).images[0]

    @timer
    def generate_image(self, *, prompt: str, negative_prompt: str, width: int, height: int, scheduler: str = None,
                       skip: int = None, scale: float = None, steps: int = None, seed: str = None):
        filename = datetime.now().strftime("%d-%b-%Y_%H-%M-%S") + f'.{self.file_format}'
        filepath = "images/" + filename
        # model settings
        self._set_scheduler(scheduler)

        self._set_clip_skip(skip - 1 if skip else Config.default_clip_skip - 1)
        generator = torch.Generator("cuda").manual_seed(Parser.get_seed(seed)) if seed else None
        self._get_image(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            scale=scale if scale else Config.default_guidance_scale,
            steps=steps if steps else Config.default_num_inference_steps,
            generator=generator
        ).save(filepath, quality=self.quality)
        return filename, filepath

    def _set_clip_skip(self, skip):
        self.pipe.text_encoder = CLIPTextModel.from_pretrained(self.repository,
                                                               subfolder="text_encoder", num_hidden_layers=12 - skip,
                                                               torch_dtype=self.torch_dtype)

    def _set_scheduler(self, scheduler):
        if not self.pipe.scheduler.__class__.__name__ == scheduler:
            self.pipe.scheduler = self._get_scheduler(scheduler)
            self.pipe.scheduler.to('cuda')

    # noinspection SpellCheckingInspection
    def _get_scheduler(self, scheduler):
        if scheduler == 'DPMSolverMultistepScheduler':
            return DPMSolverMultistepScheduler.from_config(self.pipe.scheduler.config)
        elif scheduler == 'EulerAncestralDiscreteScheduler':
            return EulerAncestralDiscreteScheduler.from_config(self.pipe.scheduler.config)
        elif scheduler == 'KDPM2DiscreteScheduler':
            return KDPM2DiscreteScheduler.from_config(self.pipe.scheduler.config)
        elif scheduler == 'UniPCMultistepScheduler':
            return UniPCMultistepScheduler.from_config(self.pipe.scheduler.config)
        elif scheduler == 'DDPMScheduler':
            return DDPMScheduler.from_config(self.pipe.scheduler.config)
        elif scheduler == 'HeunDiscreteScheduler':
            return HeunDiscreteScheduler.from_config(self.pipe.scheduler.config)
        elif scheduler == 'KDPM2AncestralDiscreteScheduler':
            return KDPM2AncestralDiscreteScheduler.from_config(self.pipe.scheduler.config)
        elif scheduler == 'DEISMultistepScheduler':
            return DEISMultistepScheduler.from_config(self.pipe.scheduler.config)
        elif scheduler == 'PNDMScheduler':
            return PNDMScheduler.from_config(self.pipe.scheduler.config)
        elif scheduler == 'DDIMScheduler':
            return DDIMScheduler.from_config(self.pipe.scheduler.config)
        elif scheduler == 'DPMSolverSinglestepScheduler':
            return DPMSolverSinglestepScheduler.from_config(self.pipe.scheduler.config)
        elif scheduler == 'LMSDiscreteScheduler':
            return LMSDiscreteScheduler.from_config(self.pipe.scheduler.config)
        elif scheduler == 'EulerDiscreteScheduler':
            return EulerDiscreteScheduler.from_config(self.pipe.scheduler.config)
        else:
            raise ValueError(f"Unsupported scheduler type {scheduler}")

    @property
    def model_name(self):
        return self.name

    @property
    def compatible(self):
        return [f"{i.__name__}" for i in self.pipe.scheduler.compatibles]
