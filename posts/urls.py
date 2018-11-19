from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostList.as_view(), name='list'),
    path('new/', views.PostCreate.as_view(), name='create'),
    path('<int:pk>/', views.PostDetail.as_view(), name='detail'),
    path('<int:pk>/edit/', views.PostUpdate.as_view(), name='update'),
    path('<int:pk>/delete/', views.PostDelete.as_view(), name='delete'),
]