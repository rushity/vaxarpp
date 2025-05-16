import logging
import json
import datetime
import os

class CustomJSONFormatter:

    @staticmethod
    def CreateLog(log_type, message, status_code, lineno, extra=None):
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "type": log_type,
            "status": status_code,
            "line": lineno,
            "message": message,
            "extra": extra
        }
        os.makedirs("logs", exist_ok=True)
        with open("logs/app.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")