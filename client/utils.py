import time

def get_timestamp():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

def format_message(session_id, message):
    timestamp = get_timestamp()
    return f"[{timestamp}] {session_id}: {message}"