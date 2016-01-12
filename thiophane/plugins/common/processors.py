
""" Common processor functions for thiophane plugins """

import re


def bool_processor(value, key, config):
    """Transforms known strings to appropriate bool values."""
    if re.match('[yY]es|[tT]rue|[yY]', value):
        return True
    elif re.match('[nN]o|[fF]alse|[nN]', value):
        return False
    else:
        return value
