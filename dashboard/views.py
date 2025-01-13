from django.shortcuts import render

# Create your views here.
def content_page(request):
    return render(request, 'dashboard/content.html')


def create_page(request):
    return render(request, 'dashboard/create.html')


def community_page(request):
    return render(request, 'dashboard/community.html')