
import json
from datetime import datetime

def gen_occurances(occurances, day=None):
    if day is None:
        day = datetime.today().date()

    dict = {}
    dict[str(day)] = occurances

    return json.dumps(dict)

