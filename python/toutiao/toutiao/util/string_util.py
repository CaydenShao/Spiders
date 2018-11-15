
def concat_str(main, content):
    if main == None:
        if content == None:
            return None
        else:
            return content
    else:
        if content == None:
            return main
        else:
            return main + content