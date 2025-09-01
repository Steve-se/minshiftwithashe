from django.urls import path
from .views import subscribe_to_newsletter, unsubscribe

app_name = 'newsletter'
urlpatterns = [
    path('subscribe/', subscribe_to_newsletter, name='subscribe'),
    path('unsubscribe/', unsubscribe, name='unsubscribe'),
]