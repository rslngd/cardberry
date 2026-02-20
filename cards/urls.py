from django.urls import path
from . import views

urlpatterns = [
    path('', views.deck_list, name='deck_list'),
    path('deck/<int:pk>/', views.deck_detail, name='deck_detail'),
    path('deck/<int:pk>/train/', views.train_deck, name='train_deck'),
    path('deck/<int:pk>/quiz/', views.quiz_deck, name='quiz_deck'),
    path('deck/<int:pk>/add/', views.card_create, name='card_create'),
]