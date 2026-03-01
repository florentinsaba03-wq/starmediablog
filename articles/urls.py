from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="home"),

    path('article/<slug:slug>/', views.article_detail, name="article_detail"),

    path('category/<slug:slug>/', views.category_articles, name='category_articles'),

    path('like/<slug:slug>/', views.like_article, name='like_article'),
    path('like/<slug:slug>/', views.like_article, name='like_article'),
    path('author/<str:username>/', views.author_profile, name="author_profile"),

]