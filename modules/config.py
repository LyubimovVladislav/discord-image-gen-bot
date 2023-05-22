import json
import os
import shutil


class Config:
    try:
        if not os.path.exists('config.json'):
            print('No config file detected, creating one...')
            shutil.copy('example_config.json', 'config.json')

            with open('config.json', 'r') as f:
                data = json.load(f)

            input_token = input('Please provide the discord API access token:\n>').strip()
            data['key'] = input_token

            with open('config.json', 'w') as f:
                json.dump(data, f, indent=2)

        with open('config.json', 'r') as f:
            config = json.load(f)

        key = config['key']
        default_guidance_scale = config['default_guidance_scale']
        default_num_inference_steps = config['default_num_inference_steps']
        default_scheduler = config['default_scheduler']
        default_clip_skip = config['default_clip_skip']
        default_resolution = config['default_resolution']
        trigger_words = config['trigger_words']
        guild = config['guild_id']
        command_prefix = config['command_prefix']
        file_format = config['file_format']
        image_save_quality = config['image_save_quality']
        repository = config['remote_repo_id_or_local_repo_path']
        half_precision_float = config['half_precision_float']

    except KeyError as e:
        raise KeyError(f'Cant find {e} value. Update your config file.')
    except (FileNotFoundError, OSError) as e:
        raise FileNotFoundError(f'Cant open a config file {e}')
