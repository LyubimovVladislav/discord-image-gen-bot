import discord
from discord import ui

from modules.config import Config
from modules.parser import Parser


class Modal(ui.Modal):
    def __init__(self, sampler, skip, resolution, gen_image):
        super().__init__(title='question')
        self.gen_image = gen_image
        self.sampler = sampler
        self.skip = skip
        self.resolution = resolution
        self.prompt = ui.TextInput(label='Prompt', style=discord.TextStyle.paragraph)
        self.n_prompt = ui.TextInput(label='Negative prompt', style=discord.TextStyle.paragraph, required=False)
        self.scale = ui.TextInput(label='Guidance Scale', default=str(Config.default_guidance_scale), max_length=5)
        self.steps = ui.TextInput(label='Sampling steps', default=str(Config.default_num_inference_steps), max_length=5)
        self.seed = ui.TextInput(label='Seed', required=False, max_length=20)
        ui.View.add_item(self, item=self.prompt)
        ui.View.add_item(self, item=self.n_prompt)
        ui.View.add_item(self, item=self.scale)
        ui.View.add_item(self, item=self.steps)
        ui.View.add_item(self, item=self.seed)

    async def on_submit(self, interaction: discord.Message.interaction):
        width, height = str(self.resolution).split('x')
        self.sampler = str(self.sampler)
        self.skip = str(self.skip)
        self.skip = int(self.skip) if self.skip and Parser.is_int(self.skip) else None
        self.scale = str(self.scale)
        self.scale = float(self.scale) if self.scale and Parser.is_float(self.scale) else None
        self.seed = str(self.seed)
        self.steps = str(self.steps)
        self.steps = int(self.steps) if self.steps and Parser.is_int(self.steps) else None
        self.prompt = str(self.prompt)
        self.n_prompt = str(self.n_prompt)
        await self.gen_image(interaction=interaction, sampler=self.sampler, skip=self.skip, width=int(width),
                             height=int(height), prompt=self.prompt, n_prompt=self.n_prompt, scale=self.scale,
                             steps=self.steps, seed=self.seed)
