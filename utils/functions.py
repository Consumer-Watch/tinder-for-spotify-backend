from datetime import datetime, timedelta
import random
import string

def generate_random_id(length=10):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

def get_future_date(start_date: datetime, days: int = 30):
    DEFAULT_UPDATE_INTERVAL_DAYS = days
    DEFAULT_UPDATE = start_date + timedelta(days = DEFAULT_UPDATE_INTERVAL_DAYS)
    return DEFAULT_UPDATE