from django.urls import path
from .views import home, detail, subscribe_to_newsletter, like_vlog
app_name = 'blog'
urlpatterns = [
    path('', home, name='home'),
    path('<str:slug>/', detail, name='detail-page'),
    path('subscribe', subscribe_to_newsletter, name='subcribe'),
    path('like/<int:vlog_id>/', like_vlog, name='like-vlog'),
]