import json
import os
import shutil
import discord


class Config:
    def __init__(self):
        try:
            if not os.path.exists('../config.json'):
                print('No config file detected, creating one...\n')
                shutil.copy('../example_config.json', 'config.json')

                with open('../config.json', 'r') as file:
                    data = file.read()

                input_token = input("Provide the discord API access token: ").strip()
                new_data = data.replace('Your_token_here', input_token)

                with open('../config.json', 'w') as file:
                    file.write(new_data)

            with open('../config.json') as f:
                config = json.load(f)

            self.guild = discord.Object(id=config['guild_id'])
            self.default_negative_sfw = config['default_sfw_negative_prompt']
            self.default_negative_nsfw = config['default_nsfw_negative_prompt']
            self.example_text = config['example']
            self.height = config['default_height']
            self.width = config['default_width']
            self.command_prefix = config['command_prefix']
            self.file_format = config['file_format']
            self.half_precision_float = config['half_precision_float']
            self.image_save_quality = config['image_save_quality']
            self.repository = config['remote_repo_id_or_local_repo_path']
            self.key = config['key']

        except KeyError as e:
            print(f'Cant find key value! Update your config file!\n{e}')
            exit(1)
        except (FileNotFoundError, OSError) as e:
            print(f'Cant open a config file.\n{e}')
            exit(1)
