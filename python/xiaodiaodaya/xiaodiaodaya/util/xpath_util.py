
def get_select_first_str(selector, xpath_str, default):
    if selector != None:
        e = selector.xpath(xpath_str)
        if e != None:
            return e.extract_first()
        else:
            return default
    else:
        return default