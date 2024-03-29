from django.urls import path
from .views import (
    PostListView,  
    PostCreateView,
    PostUpdateView,
    PostDetailView,
    PostDeleteView,
    SearchResultsView,
    TaggedPostListView
    )

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('search/', SearchResultsView.as_view(), name='search-results'),
    path('tags/<str:tag_name>/', TaggedPostListView.as_view(), name='tagged-posts-list'),
]
