# discord-image-gen-bot

This is a small discord bot that can generate images from text using Stable Diffusion pretrained models.
<hr>

# What is required?

1. Installed [Python](https://www.python.org/)
2. Installed [Git](https://git-scm.com/downloads)
3. An Nvidia GPU(preferably with 8gb vram) or AMD GPU with installed ROCm kernel driver(currently linux only)
    * Image inference can be done on CPU, but it would be painfully slow
4. A Discord bot API [token](https://discord.com/developers/applications)

# How to run:

1. Clone the repository with:
   ```
   git clone https://github.com/LyubimovVladislav/discord-image-gen-bot.git
   ```
2. Change directory into the newly created folder:
   ```
   cd discord-image-gen-bot
   ```
3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the bot with:
   ```
   python main.py
   ```

# How to configure the bot?

You can configure the bot in `config.json` file. Note that this file generates when it's missing on each run. You can
manually edit there your Discord API token, server id and more.