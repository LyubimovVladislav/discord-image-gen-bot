import discord
from discord import ui


class Modal(ui.Modal):
    def __init__(self, sampler, skip, resolution, gen_image):
        super().__init__(title='question')
        self.gen_image = gen_image
        self.sampler = sampler
        self.skip = skip
        self.resolution = resolution
        self.prompt = ui.TextInput(label='Prompt', style=discord.TextStyle.paragraph)
        self.n_prompt = ui.TextInput(label='Negative prompt', style=discord.TextStyle.paragraph, required=False)
        self.scale = ui.TextInput(label='Guidance Scale', default='7.5', max_length=5)
        self.steps = ui.TextInput(label='Sampling steps', default='50', max_length=5)
        self.seed = ui.TextInput(label='Seed', required=False, max_length=20)
        ui.View.add_item(self, item=self.prompt)
        ui.View.add_item(self, item=self.n_prompt)
        ui.View.add_item(self, item=self.scale)
        ui.View.add_item(self, item=self.steps)
        ui.View.add_item(self, item=self.seed)

    async def on_submit(self, interaction: discord.Message.interaction):
        width, height = self.resolution.split('x')
        await self.gen_image(interaction=interaction, sampler=self.sampler, skip=self.skip, width=width,
                             height=height, prompt=self.prompt, n_prompt=self.n_prompt, scale=self.scale,
                             steps=self.steps, seed=self.seed)
