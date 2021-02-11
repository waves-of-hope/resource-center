from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('videos/', views.VideoListView.as_view(), name='videos'),
    path('v/<slug:slug>/', views.VideoDetailView.as_view(), name='video')
]