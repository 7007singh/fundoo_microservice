from celery import Celery
import smtplib, ssl, os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()
redis_url = 'redis://127.0.0.1:6379/0'

celery = Celery(__name__, broker=redis_url, backend=redis_url, broker_connection_retry_on_startup=True)


@celery.task()
def send_mail(recipient, data):
    message = EmailMessage()
    message['From'] = os.environ.get('EMAIL_HOST_USER')
    message['To'] = recipient
    message['Subject'] = 'Verified'
    message.set_content(data)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(user=os.environ.get('EMAIL_HOST_USER'), password=os.environ.get('EMAIL_HOST_PASSWORD'))
        smtp.sendmail(os.environ.get('EMAIL_HOST_USER'), recipient, message.as_string())
        smtp.quit()
    return 'send mail successfully'
