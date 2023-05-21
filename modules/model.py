from datetime import datetime
import sys
import random
import re as regex

from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler, EulerAncestralDiscreteScheduler, \
    KDPM2DiscreteScheduler, UniPCMultistepScheduler, DDPMScheduler, HeunDiscreteScheduler, \
    KDPM2AncestralDiscreteScheduler, DEISMultistepScheduler, PNDMScheduler, DDIMScheduler, \
    DPMSolverSinglestepScheduler, LMSDiscreteScheduler, EulerDiscreteScheduler
import torch
from transformers import CLIPTextModel

from decorators.timer import timer


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
        self.pipe.to('cuda')
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
    def generate_image(self, *, prompt, negative_prompt, width=512, height=768, sampler=None, skip=None, scale=None,
                       steps=None, seed=None):
        filename = datetime.now().strftime("%d-%b-%Y_%H-%M-%S") + f'.{self.file_format}'
        filepath = "images/" + filename
        # model settings
        self._set_sampler(sampler)
        self._set_clip_skip(skip)
        generator = torch.Generator("cuda").manual_seed(self.get_seed(seed)) if seed else None
        self._get_image(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            scale=float(scale) if self.is_float(scale) else 7.5,
            steps=int(steps) if steps and steps.is_digit() else 50,
            generator=generator
        ).save(filepath, quality=self.quality)
        return filename, filepath

    def _set_clip_skip(self, skip):
        self.pipe.text_encoder = CLIPTextModel.from_pretrained(self.repository,
                                                               subfolder="text_encoder", num_hidden_layers=12 - skip,
                                                               torch_dtype=self.torch_dtype)

    def _set_sampler(self, scheduler):
        self.pipe.scheduler = self._get_sampler(scheduler)

    # noinspection SpellCheckingInspection
    def _get_sampler(self, scheduler):
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

    @staticmethod
    def in_maxsize_range(s: str) -> bool:
        return len(s) <= len(str(sys.maxsize))

    @staticmethod
    def is_proper_int(s: str) -> bool:
        # As seed, torch accepts only long int, so it's required to parse string to int but not exceed the long range
        # -9300000000000000000 already throws an exception(19 digits + sign) while 9999999999999999999 not(19 digits)
        # for long int type
        if not Model.in_maxsize_range(s):
            return False
        if s[0] in ('-', '+'):
            return s[1:].isdigit()
        return s.isdigit()

    @staticmethod
    def get_seed(s: str) -> int:
        if not s:
            raise ValueError('get_seed() exception: argument cant be empty')
        if Model.is_proper_int(s):
            return int(s)
        random.seed(s)
        return random.randrange(int('-' + '9' * (len(str(sys.maxsize)) - 1)), int('9' * len(str(sys.maxsize))))

    @staticmethod
    def is_float(s: str) -> bool:
        if not s:
            return False
        return not regex.match(r'^[+-]?\d+\.\d*$', s) is None
