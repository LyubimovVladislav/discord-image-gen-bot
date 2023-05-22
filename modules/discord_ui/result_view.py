import discord
from discord import ui


class ModalButton(ui.Button):
    def __init__(self, label):
        super().__init__(label=label)

    async def callback(self, i: discord.Message.interaction):
        await i.response.send_message(
            f'Model: {self.view.name}\n'
            f'Prompt:{self.view.prompt.strip()}\n'
            f'Negative prompt: {self.view.n_prompt.strip() if self.view.n_prompt and self.view.n_prompt.strip() else "NONE"}\n'
            f'Resolution: {self.view.width}x{self.view.height}\n'
            f'Sampler: {self.view.sampler}\n'
            f'Inference steps: {self.view.steps}\n'
            f'CLIP skip: {self.view.skip}\n'
            f'Guidance scale: {self.view.scale}\n'
            f'{f"Seed: {self.view.seed}" if self.view.seed and self.view.seed.strip() else ""}', ephemeral=True
        )


class ShowResult(ui.View):
    def __init__(self, *, prompt, n_prompt, width, height, sampler, steps, skip, scale, seed, name):
        super().__init__()
        self.prompt = prompt
        self.n_prompt = n_prompt
        self.width = width
        self.height = height
        self.sampler = sampler
        self.steps = steps
        self.skip = skip
        self.scale = scale
        self.seed = seed
        self.name = name
        bn = ModalButton(label='Show all settings')
        self.add_item(bn)
