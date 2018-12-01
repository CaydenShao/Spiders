from config.source_type_config import SOURCE_TYPES
from config.source_type_config import PICTURE_PAGE_URL_HEAD

def get_source_type(url):
    if SOURCE_TYPES.__contains__(url):
        return SOURCE_TYPES.get(url)
    else:
        return '0'

def get_picture_page_url_head(url):
    if PICTURE_PAGE_URL_HEAD.__contains__(url):
        return PICTURE_PAGE_URL_HEAD.get(url)
    else:
        return None