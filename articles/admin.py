from django.contrib import admin
from .models import Article, Category, Comment
from .models import Like

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Like)