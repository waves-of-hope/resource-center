from django.urls import path

from . import views

urlpatterns = [
    path('', views.VideoListView.as_view(), name='videos'),
    path('<slug:slug>/', views.VideoDetailView.as_view(), name='video')
]