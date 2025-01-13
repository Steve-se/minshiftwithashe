from django.urls import path
from .views import content_page, create_page, community_page


app_name = 'dashboard'
urlpatterns = [
  path('', content_page, name='content_page'),
  path('create/', create_page, name='create_page'),
  path('community/', community_page, name='community_page'),

]