from flask_mail import Mail
from config.app import app
from os import getenv


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'fortunealebiosu710@gmail.com'
app.config['MAIL_PASSWORD'] = "faoj owey blnx twxr"
app.config['MAIL_DEFAULT_SENDER'] = 'fortunealebiosu710@gmail.com'

print(getenv("MAIL_USERNAME"))
print(getenv("MAIL_PASSWORD"))

mail = Mail(app)