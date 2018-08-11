import json
from datetime import datetime

def json_response(status, data):
    utc_time = datetime.utcnow().isoformat()

    res = {
        "time": utc_time,
        "status": status,
        "data": data
    }

    return json.dumps(res)
