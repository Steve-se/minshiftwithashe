from django.db import models
from ckeditor.fields import RichTextField
import uuid
from django.core.mail import send_mass_mail
from django.conf import settings
from django.utils.html import strip_tags


class Subscribers(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    subscribed = models.BooleanField(default=True)
    unsubscribed_token = models.CharField(max_length=64, unique=True, blank=True, null=True)

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'

  
    def save(self, *args, **kwargs):
        if not self.unsubscribed_token:
            self.unsubscribed_token = uuid.uuid4().hex
        super().save(*args, **kwargs)
    

class EmailTemplate(models.Model):
    subject = models.CharField(max_length=255)
    message = RichTextField()
    recipient = models.ManyToManyField('Subscribers')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Call the original save first (so we have an ID for M2M)
        super().save(*args, **kwargs)

        # Now send the email to all recipients
        recipients = self.recipient.all().values_list('email', flat=True)
        sender = settings.EMAIL_HOST_USER
        plain_message = strip_tags(self.message)
        messages = [
            (self.subject, plain_message, sender, [email])
            for email in recipients
        ]
        send_mass_mail(messages, fail_silently=False)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Email Template'
        verbose_name_plural = 'Email Templates'

