from django.urls import path
from .views import home,get_bible_verse, detail, like_post
app_name = 'blog'
urlpatterns = [
    path('', home, name='home'),
    path("get-bible-verse/", get_bible_verse, name="get_bible_verse"),
    path('<str:slug>/', detail, name='detail-page'),
    path('like/<slug:slug>/', like_post, name='like-article'),
    
    


]