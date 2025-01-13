from django.db import models
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    total_articles = models.IntegerField(editable=False, verbose_name='num of posts in this category')
    category_slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)

    @property
    def total_articles(self):
        return self.articles.filter(status='upload').count()
    @property
    def total_vlogs(self):
        return self.vlogs.filter().count()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['created']


class Vlog(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="vlogs")
    description = RichTextField()
    like = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to='videos/')


    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created']


class Article(models.Model):
    STATUS_CHOICES = (
        ('archived', 'Archived'),
        ('upload', 'Upload'),
    )

    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,  related_name="articles")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='archived')
    slug = models.SlugField(max_length=250, unique=True)
    body = RichTextField()
    likes = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    image_file = models.ImageField(upload_to='images/')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    email = models.EmailField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    name = models.CharField(max_length=80)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self) -> str:
        return f"Commented by {self.name} on {self.article} "

    def is_reply(self):
        return self.parent is not None  
    

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=2000)
    last_name = models.CharField(max_length=2000)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
