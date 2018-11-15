
def print_with_defaut(content, default):
    if content == None:
        if default == None:
            print('None')
        else:
            print(default)
    else:
        print(content)