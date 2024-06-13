from celery import shared_task
from django.core.mail import send_mail
from .models import Schedule
from django.utils import timezone

@shared_task
def send_schedule_reminder():
    now = timezone.now()
    schedules = Schedule.objects.filter(start_datetime__lte=now, reminder_sent=False)
    for schedule in schedules:
        send_mail(
            subject=f'Reminder: {schedule.title}',
            message=schedule.description,
            from_email='from@example.com',
            recipient_list=['to@example.com'],
            fail_silently=False,
        )
        schedule.reminder_sent = True
        schedule.save()