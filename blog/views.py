from .models import Category, Vlog, Article, Comment, Subscriber
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from difflib import SequenceMatcher
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.core.mail import send_mail
from common.utils import check_if_email_exists
from django.contrib import messages


def home(request):
    # Display only categories with content
    categories_with_content = Category.objects.annotate(
        num_articles=Count('articles'),
        num_vlogs=Count('vlogs')
    ).filter(Q(num_articles__gt=0) | Q(num_vlogs__gt=0))

    error1, error2, data = '', '', ''
    article_selected_category = request.GET.get("category")
    vlog_selected_category = request.GET.get("vlog-category")
    search_article = request.GET.get("search")
    search_vlog = request.GET.get("search-vlog")

    # Base queries for articles and vlogs
    article_query = Article.objects.filter(status='upload')
    vlog_query = Vlog.objects.all()

    # Apply filtering for articles
    if article_selected_category:
        article_query = article_query.filter(category__name__icontains=article_selected_category)

    if search_article:
        if not search_article.strip():
            error2 = "Please enter a valid search"
        else:
            article_query = article_query.filter(
                Q(title__icontains=search_article) |
                Q(category__name__icontains=search_article) |
                Q(body__icontains=search_article)
            )

    # Apply filtering for vlogs
    if vlog_selected_category:
        vlog_query = vlog_query.filter(category__name__icontains=vlog_selected_category)

    if search_vlog:
        if not search_vlog.strip():
            error1 = "Please enter a valid search"
        else:
            vlog_query = vlog_query.filter(
                Q(title__icontains=search_vlog) |
                Q(category__name__icontains=search_vlog) |
                Q(description__icontains=search_vlog)
            )

    # Pagination for vlogs
    vlog_paginator = Paginator(vlog_query, 2) 
    vlog_page = request.GET.get('vlog_page', 1)
    try:
        vlogs = vlog_paginator.page(vlog_page)
    except PageNotAnInteger:
        vlogs = vlog_paginator.page(1)
    except EmptyPage:
        vlogs = vlog_paginator.page(vlog_paginator.num_pages)

    # Pagination for articles
    article_paginator = Paginator(article_query, 10) 
    article_page = request.GET.get('article_page', 1)
    try:
        articles = article_paginator.page(article_page)
    except PageNotAnInteger:
        articles = article_paginator.page(1)
    except EmptyPage:
        articles = article_paginator.page(article_paginator.num_pages)

    # Handle AJAX requests
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        vlogs_html = render_to_string('blog/partials/vlogs_list.html', {'all_vlog': vlogs})
        articles_html = render_to_string('blog/partials/articles_list.html', {'all_articles': articles})
        return JsonResponse({'vlogs_html': vlogs_html, 'articles_html': articles_html})

    # Render the full page for regular requests
    context = {
        'all_categories': categories_with_content,
        'vlog_selected_category': vlog_selected_category,
        'article_selected_category': article_selected_category,
        'vlogs': vlogs,
        'articles': articles,
        'error1': error1,
        'error2': error2,
        'data': data,
    }
    return render(request, 'blog/blog.html', context=context)


# ================================ DETAIL PAGE ============================================
def detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status='upload')

    previous_article = Article.objects.filter(id__lt=article.id, status='upload').order_by('-id').first()
    next_article = Article.objects.filter(id__gt=article.id, status='upload').order_by('id').first()

    # Get articles with the same category as the current article
    similar_articles = Article.objects.filter(category=article.category)
    similar_articles = similar_articles.exclude(slug=article.slug)
    similar_vlogs = Vlog.objects.filter(category=article.category)
    
    # Compute similarity based on title
    similarity_threshold = 0.3
    similar_articles_filtered = []
    for x in similar_articles:
        body_similarity = SequenceMatcher(None, article.body, x.body).ratio()
        article_similarity = SequenceMatcher(None, article.title, x.title).ratio()
        similarity_ratio = body_similarity + article_similarity
        print(similarity_ratio, '-------------------------------')
        if similarity_ratio >= similarity_threshold:
            similar_articles_filtered.append(x)
    similar_articles_filtered = similar_articles_filtered[:4]

    # compute similarity for vid based on title 
    vid_similarity_threshold1 = 0.3
    vid_similar_vlog_filtered = []
    for x in similar_vlogs:
        vid_similarity_ratio = SequenceMatcher(None, article.title, x.title).ratio()
        if vid_similarity_ratio >= vid_similarity_threshold1:
            vid_similar_vlog_filtered.append(x)
    vid_similar_vlog_filtered = vid_similar_vlog_filtered[:4]

    # Handle comment submission (POST request)
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        body = request.POST.get('body')
        parent_id = request.POST.get('parent_id')

        if name and email and body:  # Ensure all fields are provided
            # Handle parent comment or reply
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
                comment = Comment(article=article, parent=parent_comment, name=name, email=email, body=body)
            else:
                comment = Comment(article=article, name=name, email=email, body=body)

            comment.save() 

            # Redirect back to the same article page after submission
            return redirect('blog:detail-page', slug=article.slug)

    # Get total comments and parent comments
    total_comments_count = Comment.objects.filter(article=article, active=True).count()
    parent_comments = Comment.objects.filter(article=article, parent=None, active=True)

    # Pass data to the context
    context = {
        "article": article,
        "previous_article": previous_article,
        "next_article": next_article,
        "similar_articles_filtered": similar_articles_filtered,
        "similar_vlog_filtered": vid_similar_vlog_filtered,
        "comments": parent_comments,
        "total_comments": total_comments_count
    }

    return render(request, 'blog/blogpost.html', context)



# =============================== SUBSCRIBE TO NEWSLETTER ===========================================


def subscribe_to_newsletter(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")

        # Check if email already exists
        if Subscriber.objects.filter(email=email).exists():
            messages.error(request, "This email already exists!")
            return redirect('blog:home')

        # Notify the subscriber via email
        subject = "Thank you for subscribing"
        message = f"Hi {first_name}, you have successfully subscribed to our newsletter."
        sender_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        sent = send_mail(subject, message, sender_email, recipient_list)
        if sent:
            # Save the subscriber
            Subscriber.objects.create(email=email, first_name=first_name, last_name=last_name)
            messages.success(request, "Successfully subscribed!")
        else:
            messages.error(request, "Failed to send subscription email. Please try again.")

        return redirect('blog:home')

    return render(request, 'base.html')



# ============================== LIKE SYSTEM ================================
def like_vlog(request, vlog_id):
    vlog = get_object_or_404(Vlog, id=vlog_id)

    # Check if this vlog has already been liked by the user
    liked_vlogs = request.session.get('liked_vlogs', [])
    if vlog_id in liked_vlogs:
        return JsonResponse({'liked': False, 'message': 'You have already liked this!', 'likes_count': vlog.likes})

    # Increment likes and save
    vlog.likes += 1
    vlog.save()

    # Mark this vlog as liked in the session
    liked_vlogs.append(vlog_id)
    request.session['liked_vlogs'] = liked_vlogs

    return JsonResponse({'liked': True, 'likes_count': vlog.likes})

