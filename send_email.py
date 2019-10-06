import smtplib

from config import SENDER_EMAIL, RECEIVER_EMAIL, PASSWORD
from logs import LOGGER
from email.message import EmailMessage


def send_email(subject: str, message: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg.set_content(message)

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        authorization = server.login(SENDER_EMAIL, PASSWORD)
        send_message = server.send_message(msg)
        server.close()
        LOGGER.debug(
            f"Successfully sent email notification to {RECEIVER_EMAIL} from {SENDER_EMAIL}"
        )

    except smtplib.SMTPAuthenticationError as auth_error:
        LOGGER.exception(auth_error.smtp_error)
