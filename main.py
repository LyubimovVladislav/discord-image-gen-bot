import discord
import asyncio
from discord.ext import commands
from discord import app_commands
import json

from model import Model

synced = False
generates = False
try:
    with open('config.json') as f:
        config = json.load(f)
except Exception as e:
    print(e)
    exit(1)
GUILD_OBJ = discord.Object(id=config['guild_id'])
DEFAULT_NEGATIVE = config['default_negative_prompt']
EXAMPLE = config['example']
DEFAULT_HEIGHT = config['default_height']
DEFAULT_WIDTH = config['default_width']
client = commands.Bot(intents=discord.Intents.all(), command_prefix=config['command_prefix'])


@client.event
async def on_ready():
    await client.wait_until_ready()
    if not synced:
        try:
            await client.tree.sync(guild=GUILD_OBJ)
        except Exception as e:
            print(e)
    print(f'Logged in as {client.user}')
    print('Ready!')


@client.tree.command(name='example', description='See usage example', guild=GUILD_OBJ)
async def example(interaction: discord.Message.interaction):
    await interaction.response.send_message(EXAMPLE)


@client.tree.command(name='image', description='Generate an image', guild=GUILD_OBJ)
@app_commands.describe(prompt='Tags to include', negative_prompt='Tags to exclude')
async def generate(interaction: discord.Message.interaction, prompt: str, negative_prompt: str = DEFAULT_NEGATIVE,
                   height: int = DEFAULT_HEIGHT, width: int = DEFAULT_WIDTH):
    global model
    global generates
    if generates:
        await interaction.response.send_message('Wait until the previous request completes')
    generates = True
    await interaction.response.defer(thinking=True)
    filename = await asyncio.to_thread(model.get_save_image, prompt=prompt, negative_prompt=negative_prompt,
                                       height=height, width=width)
    try:
        await interaction.followup.send(file=discord.File(filename=filename, fp=filename))
    except Exception as e:
        await interaction.followup.send(f'An error occurred: {e}')
        generates = False
    generates = False


@client.tree.command(name='reset', description='Resets the bot', guild=GUILD_OBJ)
async def reset(interaction: discord.Message.interaction):
    global generates
    generates = False
    await interaction.response.send_message('Done!')


if __name__ == '__main__':
    model = Model(file_format=config['file_format'])
    client.run(config['key'])
