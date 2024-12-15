from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from celery import shared_task
from .helpers import (get_data, get_message, check_instance)
from config.settings import base

User = get_user_model()

@shared_task(bind=True)
def print_pattern(self, iterations:int):
    for turn in range(iterations):
        print('*' * turn, sep="", end="\n")
    return "Done"


@shared_task(bind=True)
def send_remainder_mail_at_6_pm(self):
    email_subject = "Crello Reminder 2: Update tasks for today!!"
    users = User.objects.filter(is_deleted=False).values('email', 'first_name', 'last_name')

    for user in users:
        to_email = user['email']
        email_body = f"Hi {user['first_name']},\n\n"

        status = check_instance(to_email)

        if status:
            email_body = "Looks like you have some assigned tasks under your name!\n\n"
            email_body += "Don't forget to update the status of your tasks today without fail :)"
        else:
            email_body = "Relax and have some of cup of your favourite beverage!\n\n"
            email_body += "You have don't have any assigned tasks under your name :)"

        email_body += "\n\nThanks & Regards,\nCrello Bot"

        send_mail(
            subject=email_subject,
            message=email_body,
            from_email=base.EMAIL_HOST_USER,
            recipient_list=[to_email,],
            fail_silently=True,
        )
        
    return "remainder 2 mails sent"

@shared_task(bind=True)
def send_remainder_mail_at_9_am(self):
    email_subject = "Crello Reminder 1: Tasks to work on today!!"
    users = User.objects.filter(is_deleted=False).values('email', 'first_name', 'last_name')

    for user in users:
        to_email = user['email']
        email_body = f"Hi {user['first_name']},\n\n"

        data = get_data(to_email)

        if len(data) == 0:
            email_body += f"Cheers!! You don't have any assigned tasks for today.\n\n"
            email_body += f"Pls check with your manager or scrum master for tasks."
        else:
            email_body += f"Here are the tasks assigned to you for today,\n\n"
            email_body += get_message(data)

        email_body += "\n\nThanks & Regards,\nCrello Bot"

        send_mail(
            subject=email_subject,
            message=email_body,
            from_email=base.EMAIL_HOST_USER,
            recipient_list=[to_email,],
            fail_silently=True,
        )
        
    return "remainder 1 mails sent"

