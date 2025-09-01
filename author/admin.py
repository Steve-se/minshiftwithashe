from django.contrib import admin
from .models import Author
# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')
    list_filter = ('name',)
    prepopulated_fields = {'name': ('email',)}
    
    def has_add_permission(self, request):
        return True