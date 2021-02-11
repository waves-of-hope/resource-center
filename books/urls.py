from django.urls import path

from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='books'),
    path('<slug:slug>/', views.BookDetailView.as_view(), name='book'),
]