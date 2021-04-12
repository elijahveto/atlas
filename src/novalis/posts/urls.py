from django.urls import path
from .views import (
    post_create_view,
    all_posts_view,
    detailed_post_view,
    section_create_view,
    like_view,
    section_view,
    PostUpdateView,
    PostDeleteView,
    SectionUpdateView,
    SectionDeleteView,
    superuser_view,
)


app_name = 'posts'

urlpatterns = [
    path('superuser/', superuser_view, name='superuser'),
    path('create-post/', post_create_view, name='new_post'),
    path('new-section/', section_create_view, name='new_section'),
    path('posts/', all_posts_view, name='all_posts'),
    path('post/<int:id>/', detailed_post_view, name='post-detail'),
    path('section/<int:id>/', section_view, name='section-detail'),
    path('post/<int:id>/like/', like_view, name='like'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('section/<int:pk>/update', SectionUpdateView.as_view(), name='section-update'),
    path('section/<int:pk>/delete', SectionDeleteView.as_view(), name='section-delete'),
]