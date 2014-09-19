from datetime import datetime, timedelta

def natural_numbers():
    n = 0
    while True:
        yield n
        n += 1

def quarter_hourly():
    now = datetime.now()
    start = datetime(now.year, now.month, now.day, now.hour, int(now.minute / 15) * 15 + 15)
    for n in natural_numbers():
        yield start + timedelta(minutes=n * 15)

def half_hourly():
    now = datetime.now()
    start = datetime(now.year, now.month, now.day, now.hour, int(now.minute / 30) * 30 + 30)
    for n in natural_numbers():
        yield start + timedelta(minutes=n * 30)

def hourly(minute=0):
    now = datetime.now()
    start = datetime(now.year, now.month, now.day, now.hour, minute)
    if start <= now:
        start += + timedelta(hours=1)
    for n in natural_numbers():
        yield start + timedelta(hours=n)

def daily(hour=0, minute=0):
    now = datetime.now()
    start = datetime(now.year, now.month, now.day, hour, minute)
    if start <= now:
        start += + timedelta(days=1)
    for n in natural_numbers():
        yield start + timedelta(days=n)

def minutely():
    now = datetime.now()
    start = datetime(now.year, now.month, now.day, now.hour, now.minute) + timedelta(minutes=1)
    for n in natural_numbers():
        result = start + timedelta(minutes=n)
        if result < datetime.now():
            now = datetime.now()
            start = datetime(now.year, now.month, now.day, now.hour, now.minute) + timedelta(minutes=1 - n)
        yield start + timedelta(minutes=n)
