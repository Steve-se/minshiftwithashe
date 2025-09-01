from django.contrib import admin
from .models import Subscribers, EmailTemplate
from django.conf import settings
from django.core.mail import send_mail
from ckeditor.fields import RichTextField 
# Register your models here.

admin.site.register(Subscribers)

admin.site.register(EmailTemplate)

# @admin.register(NewsletterSubscription)
# class NewsletterSubscriptionAdmin(admin.ModelAdmin):
#     # list_display = ('email', 'subscribed_at', 'active')
#     # list_filter = ('active', 'subscribed_at')
#     # search_fields = ('email',)
#     # ordering = ('-subscribed_at',)

#     # def subscribed_at(self, obj):
#     #     return obj.created_at.strftime('%Y-%m-%d %H:%M:%S')
    
#     # subscribed_at.short_description = 'Subscribed At'