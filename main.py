import discord
import asyncio
from discord.ext import commands
import os

from decorators.singleton import singleton
from modules.discord_ui.result_view import ShowResult
from modules.model import Model
from modules.config import Config
from modules.discord_ui.image_params_view import ShowImageParams


@singleton
class Bot(commands.Bot):
    def __init__(self, *, command_prefix, intents, guild_id, model):
        super().__init__(command_prefix, intents=intents)
        self.guild = discord.Object(id=guild_id)
        self.model = model
        self.register_app_commands()

    def register_app_commands(self):
        @self.tree.command(name='trigger-words', description="Provides the model's trigger words", guild=self.guild)
        async def trigger_words(interaction: discord.Message.interaction):
            await interaction.response.send_message('Not implemented')

        @self.tree.command(name='example', description="Provides the civitai example", guild=self.guild)
        async def trigger_words(interaction: discord.Message.interaction):
            await interaction.response.send_message('Not implemented')

        @discord.app_commands.CommandTree.command(self=self.tree, name='image',
                                                  description='Generates an image', guild=self.guild)
        async def generate(interaction: discord.Message.interaction):
            await interaction.response.send_message(
                f'{self.model.name}:', view=ShowImageParams(self.model.compatible, gen_image=self.generate_image)
            )

    async def generate_image(self, interaction: discord.Message.interaction,
                             sampler, skip, height, width, prompt, n_prompt, scale, steps, seed):
        try:
            await interaction.response.defer(thinking=True)
            async with semaphore:
                filename, filepath = await asyncio.to_thread(self.model.generate_image,
                                                             sampler=sampler,
                                                             skip=skip,
                                                             scale=scale,
                                                             seed=seed,
                                                             steps=steps,
                                                             prompt=prompt,
                                                             negative_prompt=n_prompt,
                                                             height=height, width=width)
            content = f'Prompt: {str(prompt).strip()}'
            await interaction.followup.send(content=content,
                                            file=discord.File(filename=filename, fp=filepath),
                                            view=ShowResult(
                                                prompt=prompt, n_prompt=n_prompt, width=width,
                                                height=height, sampler=sampler, steps=steps, skip=skip, scale=scale,
                                                seed=seed
                                            ))
        except Exception as e:
            await interaction.followup.send(f'An error occurred: {e}')

    async def on_ready(self):
        await self.wait_until_ready()
        try:
            await self.tree.sync(guild=self.guild)
        except Exception as e:
            print(e)
        print(f'Logged in as {self.user}')
        print('Ready!')


if __name__ == '__main__':
    semaphore = asyncio.BoundedSemaphore(1)
    config = Config()
    folder = 'images'
    if not os.path.exists(folder):
        os.makedirs(folder)
    model = Model(
        file_format=config.file_format,
        half_precision=config.half_precision_float,
        quality=config.image_save_quality,
        repository=config.repository
    )
    bot = Bot(
        intents=discord.Intents.all(),
        command_prefix=config.command_prefix,
        guild_id=config.guild,
        model=None
    )
    bot.run(config.key)
