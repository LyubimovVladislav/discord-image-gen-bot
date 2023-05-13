import threading

import discord
import asyncio
from discord.ext import commands
from discord import app_commands
from datetime import datetime
import json
from time import sleep
import os

from model import Model

try:
    with open('config.json') as f:
        config = json.load(f)
    GUILD_OBJ = discord.Object(id=config['guild_id'])
    DEFAULT_NEGATIVE_SFW = config['default_sfw_negative_prompt']
    DEFAULT_NEGATIVE_NSFW = config['default_nsfw_negative_prompt']
    EXAMPLE = config['example']
    DEFAULT_HEIGHT = config['default_height']
    DEFAULT_WIDTH = config['default_width']
    client = commands.Bot(intents=discord.Intents.all(), command_prefix=config['command_prefix'])
except KeyError as e:
    print(f'Cant find key value! Update your config file!\n{e}')
    exit(1)
except (FileNotFoundError, OSError) as e:
    print(f'Cant open a config file!\n{e}')
    exit(1)
semaphore = asyncio.BoundedSemaphore(1)
last_active = datetime.now()


def free_memory_timer(delay: int):
    print(f'Daemon started at {datetime.now().strftime("%H:%M:%S")}')
    while True:
        sleep(delay)
        if ((last_active - datetime.now()).seconds // 60 >= 5) and model.is_active:
            print(f'vRam freed at {datetime.now().strftime("%H:%M:%S")}')
            model.delete()


@client.event
async def on_ready():
    await client.wait_until_ready()
    try:
        await client.tree.sync(guild=GUILD_OBJ)
    except Exception as e:
        print(e)
    print(f'Logged in as {client.user}')
    print('Ready!')
    thread = threading.Thread(target=free_memory_timer, args=(config['release_vram_timer_seconds'],), daemon=True)
    thread.start()


@client.tree.command(name='example', description='See usage example', guild=GUILD_OBJ)
async def example(interaction: discord.Message.interaction):
    await interaction.response.send_message(EXAMPLE)


@client.tree.command(name='image', description='Generate an image', guild=GUILD_OBJ)
@app_commands.describe(prompt='Tags to include', negative_prompt='Tags to exclude', height='Height of the image',
                       width='Width of the image')
async def generate(interaction: discord.Message.interaction, prompt: str, negative_prompt: str = DEFAULT_NEGATIVE_SFW,
                   height: int = DEFAULT_HEIGHT, width: int = DEFAULT_WIDTH):
    global last_active
    if not model.is_active:
        await asyncio.to_thread(model.init())
        print(f'vRam allocated at {datetime.now().strftime("%H:%M:%S")}')
    last_active = datetime.now()
    if type(interaction.channel) is discord.channel.TextChannel and interaction.channel.nsfw:
        if negative_prompt == DEFAULT_NEGATIVE_SFW:
            negative_prompt = DEFAULT_NEGATIVE_NSFW
    try:
        await interaction.response.defer(thinking=True)
        async with semaphore:
            filename, filepath = await asyncio.to_thread(model.get_save_image, prompt=prompt,
                                                         negative_prompt=negative_prompt,
                                                         height=height, width=width)
        if negative_prompt == DEFAULT_NEGATIVE_SFW:
            negative_prompt = 'default(SFW)'
        elif negative_prompt == DEFAULT_NEGATIVE_NSFW:
            negative_prompt = 'default(NSFW)'
        content = f'Prompt: {prompt}\nNegative prompt: ' \
                  f'{negative_prompt}' \
                  f'\nResolution: {width}x{height}'
        await interaction.followup.send(content=content, file=discord.File(filename=filename, fp=filepath))
    except ValueError as e:
        print(f'A fatal error occurred:{e}\nExiting...')
        await interaction.response.send_message(f'An error occurred: {e}')
        exit(1)
    except Exception as e:
        await interaction.response.send_message(f'An error occurred: {e}')


@client.tree.command(name='reset', description='Resets the bot', guild=GUILD_OBJ)
async def reset(interaction: discord.Message.interaction):
    await interaction.response.send_message('Done!')


if __name__ == '__main__':
    folder = 'images'
    if not os.path.exists(folder):
        os.makedirs(folder)
    model = Model(file_format=config['file_format'])
    client.run(config['key'])
