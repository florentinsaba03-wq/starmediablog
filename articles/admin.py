from django.contrib import admin
from .models import Article, Category, Comment
from .models import Like
from .models import Guide, Subscriber

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Subscriber)
@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ('title', 'downloads_count')