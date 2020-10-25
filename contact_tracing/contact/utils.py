
import json
from datetime import datetime

def gen_today_occurances(occurances):
    today = datetime.today().date()

    dict = {}
    dict[str(today)] = occurances

    return json.dumps(dict)

