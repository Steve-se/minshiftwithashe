from django.contrib import admin
from .models import Category, Vlog, Article, Comment, Subscriber

admin.site.site_header = "MindshiftWithAshe Admin Panel"
admin.site.site_title = "MindshiftWithAshe Admin"
admin.site.index_title = "Welcome to the MindshiftWithAshe Management"

admin.site.register(Subscriber)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_articles', 'total_vlogs', 'category_slug')
    prepopulated_fields = {'category_slug': ('name',)}

@admin.register(Vlog)
class VlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'like', 'created')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'created', )
    list_filter = ('status', 'created')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created'
    ordering = ('status', 'created')

    def category(self, obj):
        return obj.category
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'article', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email',)




