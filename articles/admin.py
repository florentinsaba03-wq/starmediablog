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
@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = [
        'email', 'name',
        'subscribed_at', 'is_active'
    ]
    list_filter = ['is_active']
    search_fields = ['email', 'name']