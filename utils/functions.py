from datetime import datetime, timedelta
import random
import string
from typing import List

from flask_mail import Message

from config.mail import mail

def generate_random_id(length=10):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

def get_future_date(start_date: datetime, days: int = 30):
    DEFAULT_UPDATE_INTERVAL_DAYS = days
    DEFAULT_UPDATE = start_date + timedelta(days = DEFAULT_UPDATE_INTERVAL_DAYS)
    return DEFAULT_UPDATE

def get_month_and_year(datetime_string):
  """Extracts month and year from a datetime string.

  Args:
      datetime_string: The datetime string in the format 'YYYY-MM-DDTHH:MM:SS.ffffff'.

  Returns:
      A tuple containing the month and year as strings.
  """

  # Parse the datetime string into a datetime object
  datetime_obj = datetime.strptime(datetime_string, '%Y-%m-%dT%H:%M:%S.%f')

  # Extract month and year
  month = datetime_obj.strftime('%B')  # Month in full text format
  year = str(datetime_obj.year)

  return month + " " + year

def send_email_to_user(subject: str, body: str, recipents: List[str]):
    msg = Message(
        subject=subject,
        recipients=recipents,
        body=body,
        sender=('Fortune From Sonder', 'no-reply@example.com')
    )
    mail.send(msg)
