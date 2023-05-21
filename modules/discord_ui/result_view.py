import discord
from discord import ui


class ModalButton(ui.Button):
    def __init__(self, label):
        super().__init__(label=label)

    async def callback(self, i: discord.Message.interaction):
        await i.response.send_message(
            f'Prompt:{str(self.view.prompt).strip()}\n'
            f'Negative prompt: {str(self.view.n_prompt).strip() if str(self.view.n_prompt).strip() else "NONE"}\n'
            f'Resolution: {self.view.width}x{self.view.height}\n'
            f'Sampler: {self.view.sampler}\n'
            f'Inference steps: {self.view.steps}\n'
            f'CLIP skip: {int(self.view.skip) + 1}\n'
            f'Guidance scale: {self.view.scale}\n'
            f'{f"Seed: {self.view.seed}" if str(self.view.seed).strip() else ""}'
        )


class ShowResult(ui.View):
    def __init__(self, *, prompt, n_prompt, width, height, sampler, steps, skip, scale, seed):
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
        bn = ModalButton(label='Show all settings')
        self.add_item(bn)
