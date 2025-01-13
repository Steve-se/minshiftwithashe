# from django.contrib import admin
from blog.models import Subscriber


def check_if_email_exists(email):
    a = Subscriber.objects.filter(email=email).exists()
    return a 

# # Register your models here.
# def check_if_cat_has_posts(request, category):
#     # Access the queryset with `all()` or by using `.exists()` directly on `category.articles` and `category.vlogs`
#     if category.articles.all().exists() or category.vlogs.all().exists():
#         return True
#     else:
#         return False