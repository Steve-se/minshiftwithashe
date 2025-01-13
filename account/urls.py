from django.urls import path
from .views import signin


app_name = 'account'
urlpatterns = [
  path('login/', signin, name='login'),


]