import time

# تابعی برای گرفتن timestamp
def get_timestamp():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

# تابعی برای فرمت کردن پیام‌ها با تاریخ و زمان
def format_message(username, message):
    timestamp = get_timestamp()
    return f"[{timestamp}] {username}: {message}"
