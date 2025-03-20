from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from events.models import Event

@receiver(m2m_changed, sender=Event.participants.through)
def notify_participant_on_rsvp(sender, instance, action, **kwargs):
    if action == "post_add":
        assigned_email = [emp.email for emp in instance.participants.all()]
        send_mail(
            "Event RSVP Confirmation",
            f"You are confirmed for: {instance.name}\nDate: {instance.date}\nTime: {instance.time}",
            "rokayon.cse@gmail.com",
            assigned_email,
            fail_silently=False,
        )
