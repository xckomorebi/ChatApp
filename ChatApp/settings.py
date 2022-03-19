import os

DB_NAME = "chatapp.db"
DB_PATH = os.path.join("resource", DB_NAME)

PORT_MIN = 1024
PORT_MAX = 65535

DEBUG = os.getenv("CHAT_APP_DEBUG", False)

if DEBUG:
    TIMEOUT = 1000
else:
    TIMEOUT = 0.5

