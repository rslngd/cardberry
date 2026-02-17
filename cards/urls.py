from django.urls import path
from . import views

urlpatterns = [
    path('', views.deck_list, name='deck_list'),
    path('deck/<int:pk>/', views.deck_detail, name='deck_detail'),
]