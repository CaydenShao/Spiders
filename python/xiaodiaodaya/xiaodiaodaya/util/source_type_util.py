from config.source_type_config import JOKE_TYPES

def get_joke_type(url):
    if JOKE_TYPES.__contains__(url):
        return JOKE_TYPES.get(url)
    else:
        return '0'