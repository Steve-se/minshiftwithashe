from .models import Category, Vlog, Article, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from difflib import SequenceMatcher
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
import requests
from django.views.decorators.http import require_GET



@require_GET
def get_bible_verse(request):
    ref = request.GET.get("ref", "")
    try:
        res = requests.get(f"https://bible-api.com/{ref}")
        data = res.json()
        return JsonResponse({
            "reference": data.get("reference", ref),
            "text": data.get("text", "Verse not found.")
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



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
    vlog_paginator = Paginator(vlog_query, 12) 
    vlog_page = request.GET.get('vlog_page', 1)
    try:
        vlogs = vlog_paginator.page(vlog_page)
    except PageNotAnInteger:
        vlogs = vlog_paginator.page(1)
    except EmptyPage:
        vlogs = vlog_paginator.page(vlog_paginator.num_pages)

    # Pagination for articles
    article_paginator = Paginator(article_query, 12) 
    article_page = request.GET.get('article_page', 1)
    try:
        articles = article_paginator.page(article_page)
    except PageNotAnInteger:
        articles = article_paginator.page(1)
    except EmptyPage:
        articles = article_paginator.page(article_paginator.num_pages)


    # Handle AJAX requests
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if article_selected_category or search_article:
            articles_html = render_to_string('blog/partials/articles_list.html', {'articles': articles})
            return JsonResponse({'articles_html': articles_html})
        
        elif vlog_selected_category or search_vlog:
            vlogs_html = render_to_string('blog/partials/vlogs_list.html', {'all_vlog': vlogs})
            return JsonResponse({'vlogs_html': vlogs_html})
    

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
    absolute_image_url = request.build_absolute_uri(article.image_file.url)
    absolute_post_url = request.build_absolute_uri()

    previous_article = Article.objects.filter(id__lt=article.id, status='upload').order_by('-id').first()
    next_article = Article.objects.filter(id__gt=article.id, status='upload').order_by('id').first()

    # Similar articles
    similar_articles = Article.objects.filter(category=article.category).exclude(slug=article.slug)
    similar_vlogs = Vlog.objects.filter(category=article.category)

    similarity_threshold = 0.3
    similar_articles_filtered = [
        x for x in similar_articles
        if SequenceMatcher(None, article.body, x.body).ratio() + SequenceMatcher(None, article.title, x.title).ratio() >= similarity_threshold
    ][:4]

    vid_similar_vlog_filtered = [
        x for x in similar_vlogs
        if SequenceMatcher(None, article.title, x.title).ratio() >= 0.3
    ][:4]

    # Handle comment submission (POST request)
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        body = request.POST.get('body')
        parent_id = request.POST.get('parent_id')

        if name and email and body:
            if parent_id:
                parent_comment = Comment.objects.filter(id=parent_id).first()
                comment = Comment(article=article, parent=parent_comment, name=name, email=email, body=body)
            else:
                comment = Comment(article=article, name=name, email=email, body=body)
            comment.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'name': comment.name,
                    'body': comment.body,
                    'created': timezone.localtime(comment.created).strftime('%d.%m.%Y'),
                })

            return redirect('blog:detail-page', slug=article.slug)

    total_comments_count = Comment.objects.filter(article=article, active=True).count()
    parent_comments = Comment.objects.filter(article=article, parent=None, active=True)

    context = {
        "article": article,
        "previous_article": previous_article,
        "next_article": next_article,
        "similar_articles_filtered": similar_articles_filtered,
        "similar_vlog_filtered": vid_similar_vlog_filtered,
        "comments": parent_comments,
        "total_comments": total_comments_count,
        'absolute_image_url': absolute_image_url,
        'absolute_post_url': absolute_post_url,
    }

    return render(request, 'blog/blogpost.html', context)



# ============================== LIKE SYSTEM ================================
def like_post(request, slug):
    article = get_object_or_404(Article, slug=slug, status='upload')

    # Track liked articles using session
    liked_articles = request.session.get('liked_articles', [])

    if article.id in liked_articles:
        return JsonResponse({
            'liked': False,
            'message': 'You have already liked this post!',
            'likes_count': article.likes
        })

    # Increment like count
    article.likes += 1
    article.save()

    # Save the like in session
    liked_articles.append(article.id)
    request.session['liked_articles'] = liked_articles

    return JsonResponse({
        'liked': True,
        'likes_count': article.likes,
        'message': 'Thanks for liking!'
    })
