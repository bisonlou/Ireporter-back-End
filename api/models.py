red_flags = []


def add_red_flag(red_flag):
    red_flags.append(red_flag)


def get_current_id():
    if len(red_flags) == 0:
        return 0        
    return red_flags[-1]['id']

def get_all_red_flags():
    return red_flags