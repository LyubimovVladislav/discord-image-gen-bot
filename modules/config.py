import json
import os
import shutil
from os.path import dirname


class Config:
    def __init__(self):
        try:
            if not os.path.exists(f'{dirname(__file__)}/../config.json'):
                print('No config file detected, creating one...')
                shutil.copy(f'{dirname(__file__)}/../example_config.json', f'{dirname(__file__)}/../config.json')

                with open('config.json', 'r') as f:
                    data = json.load(f)

                input_token = input('Please provide the discord API access token:\n> ').strip()
                data['key'] = input_token
                input_token = input('Please provide the server id:\n> ').strip()
                data['guild_id'] = input_token

                with open(f'{dirname(__file__)}/../config.json', 'w') as f:
                    json.dump(data, f, indent=2)

            with open(f'{dirname(__file__)}/../config.json', 'r') as f:
                config = json.load(f)

            self.key = config['key']
            self.default_guidance_scale = config['default_guidance_scale']
            self.default_num_inference_steps = config['default_num_inference_steps']
            self.default_scheduler = config['default_scheduler']
            self.default_clip_skip = config['default_clip_skip']
            self.default_resolution = config['default_resolution']
            self.trigger_words = config['trigger_words']
            self.guild = config['guild_id']
            self.command_prefix = config['command_prefix']
            self.file_format = config['file_format']
            self.image_save_quality = config['image_save_quality']
            self.repository = config['remote_repo_id_or_local_repo_path']
            self.half_precision_float = config['half_precision_float']

        except KeyError as e:
            raise KeyError(f'Cant find {e} value. Update your config file.')
        except ValueError as e:
            raise ValueError(f'Server id should consist only with digits.')
        except (FileNotFoundError, OSError) as e:
            raise FileNotFoundError(f'Cant open a config file {e}')
