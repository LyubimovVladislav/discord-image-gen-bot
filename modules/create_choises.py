from discord.app_commands import Choice


def create_sampler_choices_from_list(compatible) -> [Choice]:
    return [Choice(name=s, value=s) for s in compatible]


def create_resolution_choices() -> [Choice]:
    return [Choice(name='Square 512x512', value='512x512'),
            Choice(name='Square 768x768', value='768x768'),
            Choice(name='Square 1024x1024', value='1024x1024'),
            Choice(name='Portrait 512x768', value='512x768'),
            Choice(name='Portrait 512x1024', value='512x1024'),
            Choice(name='Portrait 768x1024', value='768x1024'),
            Choice(name='Album 768x512', value='768x512'),
            Choice(name='Album 1024x512', value='1024x512'),
            Choice(name='Album 1024x768', value='1024x768')]
