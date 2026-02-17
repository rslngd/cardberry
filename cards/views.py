from django.shortcuts import render
from .models import Deck
from django.shortcuts import render, get_object_or_404

def deck_list(request):
    # Достаем все колоды из базы данных
    # DE: alle Stapel abrufen
    decks = Deck.objects.all()
    # Передаем их в шаблон
    return render(request, 'cards/deck_list.html', {'decks': decks})

def deck_detail(request, pk):
    """
    Просмотр содержимого конкретной колоды.
    pk - это Primary Key (уникальный ID колоды в базе).
    """
    # DE: Einzelnen Stapel anhand der ID abrufen
    deck = get_object_or_404(Deck, pk=pk)
    # Получаем все карточки этой колоды
    cards = deck.cards.all() 
    return render(request, 'cards/deck_detail.html', {'deck': deck, 'cards': cards})