import os
import smtplib
import ssl
from email.message import EmailMessage
from celery import Celery
from dotenv import load_dotenv

load_dotenv()
redis_url = os.environ.get('REDIS_URL')

celery = Celery(__name__, broker=redis_url, backend=redis_url, broker_connection_retry_on_startup=True)


@celery.task()
def send_mail(recipient, data):
    message = EmailMessage()
    message['From'] = os.environ.get('EMAIL_HOST_USER')
    message['To'] = recipient
    message['Subject'] = 'Verification link'
    message.set_content(data)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(os.environ.get('MAIL_ADDRESS'), 465, context=context) as smtp:
        smtp.login(user=os.environ.get('EMAIL_HOST_USER'), password=os.environ.get('EMAIL_HOST_PASSWORD'))
        smtp.sendmail(os.environ.get('EMAIL_HOST_USER'), recipient, message.as_string())
        smtp.quit()
    return 'send mail successfully'
