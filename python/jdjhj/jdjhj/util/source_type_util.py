from config.source_type_config import JOKE_TYPES
from config.source_type_config import JOKE_PAGE_URL_HEAD

def get_joke_type(url):
    if JOKE_TYPES.__contains__(url):
        return JOKE_TYPES.get(url)
    else:
        return '0'

def get_joke_page_url_head(url):
    if JOKE_PAGE_URL_HEAD.__contains__(url):
        return JOKE_PAGE_URL_HEAD.get(url)
    else:
        return None