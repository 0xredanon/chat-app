#!/bin/bash

# راه‌اندازی سرور
python3 server/server.py &

# راه‌اندازی کلاینت
python3 client/main.py
