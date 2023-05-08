import discord
import asyncio
from discord.ext import commands
from discord import app_commands

from model import Model

GUILD_OBJ = discord.Object(id=403345142301458442)
synced = False
client = commands.Bot(intents=discord.Intents.all(), command_prefix='&')


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
    await interaction.response.send_message(
        'Prompt should be including tags.\nExample prompt: "masterpiece, best quality, 1girl, cat ears, blush,'
        ' nose blush, white hair, red eyes, smile, open mouth, white background, simple background,  hair ornament"\n' +
        'Negative-Prompt should be excluding tags.\nExample Negative-Prompt: "nsfw, nude, lowres,bad anatomy, bad hands,'
        ' error, text, missing fingers, extra digit, fewer digits, cropped,'
        ' worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry"',
    )


@client.tree.command(name='image', description='Generate an image', guild=GUILD_OBJ)
@app_commands.describe(prompt='Tags to include', negative_prompt='Tags to exclude')
async def generate(interaction: discord.Message.interaction, prompt: str, negative_prompt: str):
    global model
    filename = await asyncio.get_running_loop().run_in_executor(None, model.get_save_image(prompt=prompt,
                                                                                           negative_prompt=negative_prompt))
    await interaction.response.defer(thinking=True)
    try:
        await interaction.followup.send(file=discord.File(filename=filename, fp=filename))
    except Exception as e:
        await interaction.followup.send(f'An error occurred: {e}')


if __name__ == '__main__':
    model = Model()
    client.run()
