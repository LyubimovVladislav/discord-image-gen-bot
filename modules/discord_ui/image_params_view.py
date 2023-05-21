from typing import Any

import discord
from discord import ui, Interaction
from discord.ui import Item

from modules.discord_ui.image_params_modal import Modal


class ModalButton(ui.Button):
    def __init__(self, label, gen_image):
        super().__init__(label=label)
        self.gen_image = gen_image

    async def callback(self, i: discord.Message.interaction) -> Any:
        if self.view.sampler.values and self.view.clip_skip.values and self.view.resolution.values:
            await i.response.send_modal(
                Modal(self.view.sampler.values[0],
                      self.view.clip_skip.values[0],
                      self.view.resolution.values[0],
                      self.gen_image))
        else:
            await i.response.send_message('Set all the options', ephemeral=True)


class Menu(ui.Select):
    def __init__(self, *, placeholder, options):
        super().__init__(placeholder=placeholder, options=options)

    async def callback(self, i: discord.Message.interaction) -> Any:
        await i.response.defer()


class ShowImageParams(ui.View):
    def __init__(self, comp, gen_image):
        super().__init__()
        bn = ModalButton(label='Send', gen_image=gen_image)
        self.sampler = Menu(placeholder='Sampler', options=ShowImageParams._create_options_from_list(comp))
        self.clip_skip = Menu(placeholder='CLIP skip',
                              options=self._create_options_from_list(range(1, 8)))
        self.resolution = Menu(placeholder='Resolution',
                               options=self._create_resolution_options())
        self.add_item(self.sampler).add_item(self.clip_skip).add_item(self.resolution).add_item(bn)

    @staticmethod
    def _create_options_from_list(arr) -> [discord.SelectOption]:
        return [discord.SelectOption(label=val, value=val) for val in arr]

    @staticmethod
    def _create_resolution_options() -> [discord.SelectOption]:
        return [discord.SelectOption(label='Square 512x512', value='512x512'),
                discord.SelectOption(label='Square 768x768', value='768x768'),
                discord.SelectOption(label='Square 1024x1024', value='1024x1024'),
                discord.SelectOption(label='Portrait 512x768', value='512x768'),
                discord.SelectOption(label='Portrait 512x1024', value='512x1024'),
                discord.SelectOption(label='Portrait 768x1024', value='768x1024'),
                discord.SelectOption(label='Album 768x512', value='768x512'),
                discord.SelectOption(label='Album 1024x512', value='1024x512'),
                discord.SelectOption(label='Album 1024x768', value='1024x768')]

    async def interaction_check(self, interaction: Interaction, /) -> bool:
        return await super().interaction_check(interaction)

    async def on_timeout(self) -> None:
        await super().on_timeout()

    async def on_error(self, interaction: Interaction, error: Exception, item: Item[Any], /) -> None:
        await super().on_error(interaction, error, item)
