from config.source_type_config import SOURCE_TYPES

def get_source_type(url):
    if SOURCE_TYPES.__contains__(url):
        return SOURCE_TYPES.get(url)
    else:
        return '0'