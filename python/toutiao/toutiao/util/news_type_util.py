from config.news_type_config import NEWS_TYPES

def get_news_type(url):
    if NEWS_TYPES.__contains__(url):
        return NEWS_TYPES.get(url)
    else:
        return '0'