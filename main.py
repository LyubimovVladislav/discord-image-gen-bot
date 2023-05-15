import discord
import asyncio
from discord.ext import commands
from discord import app_commands
import os

from modules.model import Model
from modules.config import Config

config = Config()
client = commands.Bot(intents=discord.Intents.all(), command_prefix=config.command_prefix)


@client.event
async def on_ready():
    await client.wait_until_ready()
    try:
        await client.tree.sync(guild=config.guild)
    except Exception as e:
        print(e)
    print(f'Logged in as {client.user}')
    print('Ready!')


@client.tree.command(name='example', description='See usage example', guild=config.guild)
async def example(interaction: discord.Message.interaction):
    await interaction.response.send_message(config.example_text)


@client.tree.command(name='image', description='Generate an image', guild=config.guild)
@app_commands.describe(prompt='Tags to include', negative_prompt='Tags to exclude', height='Height of the image',
                       width='Width of the image')
async def generate(interaction: discord.Message.interaction, prompt: str,
                   negative_prompt: str = config.default_negative_sfw,
                   height: int = config.height, width: int = config.width):
    global model
    if type(interaction.channel) is discord.channel.TextChannel and interaction.channel.nsfw:
        if negative_prompt == config.default_negative_sfw:
            negative_prompt = config.default_negative_nsfw
    try:
        await interaction.response.defer(thinking=True)
        async with semaphore:
            filename, filepath = await asyncio.to_thread(model.get_save_image, prompt=prompt,
                                                         negative_prompt=negative_prompt,
                                                         height=height, width=width)
        if negative_prompt == config.default_negative_sfw:
            negative_prompt = 'default(SFW)'
        elif negative_prompt == config.default_negative_nsfw:
            negative_prompt = 'default(NSFW)'
        content = f'Prompt: {prompt}\nNegative prompt: ' \
                  f'{negative_prompt}' \
                  f'\nResolution: {width}x{height}'
        await interaction.followup.send(content=content, file=discord.File(filename=filename, fp=filepath))
    except Exception as e:
        await interaction.followup.send(f'An error occurred: {e}')


@client.tree.command(name='reset', description='Resets the bot', guild=config.guild)
async def reset(interaction: discord.Message.interaction):
    await interaction.response.send_message('Done!')


if __name__ == '__main__':
    semaphore = asyncio.BoundedSemaphore(1)
    folder = 'images'
    if not os.path.exists(folder):
        os.makedirs(folder)
    model = Model(
        file_format=config.file_format,
        half_precision=config.half_precision_float,
        quality=config.image_save_quality,
        repository=config.repository
    )
    client.run(config.key)
