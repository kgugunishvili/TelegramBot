

def check_addition(into: str, allowed_list: list):
    return all([x in allowed_list for x in list(into)])
