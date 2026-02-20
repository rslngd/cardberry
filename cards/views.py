import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Deck, Card
from .forms import CardForm

@login_required
def deck_list(request):
    decks = Deck.objects.filter(owner=request.user)
    return render(request, 'cards/deck_list.html', {'decks': decks})

@login_required
def deck_detail(request, pk):
    deck = get_object_or_404(Deck, pk=pk, owner=request.user)
    cards = deck.cards.all()
    return render(request, 'cards/deck_detail.html', {'deck': deck, 'cards': cards})

@login_required
def card_create(request, pk):
    deck = get_object_or_404(Deck, pk=pk, owner=request.user)
    if request.method == "POST":
        form = CardForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            card.deck = deck
            card.save()
            return redirect('deck_detail', pk=deck.pk)
    else:
        form = CardForm()
    return render(request, 'cards/card_form.html', {'form': form, 'deck': deck})

@login_required
def train_deck(request, pk):
    deck = get_object_or_404(Deck, pk=pk, owner=request.user)
    cards = deck.cards.all()
    random_card = random.choice(cards) if cards.exists() else None
    return render(request, 'cards/train.html', {'deck': deck, 'card': random_card})

# --- ЛОГИКА ПРОВЕРКИ ---
@login_required
def quiz_deck(request, pk):
    deck = get_object_or_404(Deck, pk=pk, owner=request.user)
    all_user_cards = Card.objects.filter(deck__owner=request.user)

    # Инициализация игры
    # Проверяем наличие И жизней, И очков. Если чего-то нет - создаем заново.
    if 'lives' not in request.session or 'score' not in request.session or request.GET.get('reset'):
        request.session['lives'] = 3
        request.session['score'] = 0
        request.session.modified = True # Принудительно сохраняем
    
    # Теперь безопасно достаем значения
    lives = request.session['lives']
    score = request.session['score']

    # Если мы обрабатываем ответ
    selected_id = None
    status = None
    question_card_id = request.POST.get('question_card_id')

    if request.method == "POST" and question_card_id:
        # Получаем ту же карточку, которая была в вопросе
        question_card = get_object_or_404(Card, id=question_card_id)
        selected_id = int(request.POST.get('answer_id'))
        
        # Получаем варианты из скрытого поля, чтобы они не перемешались заново
        options_ids = request.POST.get('options_ids').split(',')
        options = Card.objects.filter(id__in=options_ids)
        
        if selected_id == question_card.id:
            status = 'correct'
            request.session['score'] += 1
        else:
            status = 'wrong'
            request.session['lives'] -= 1
        
        request.session.modified = True
    else:
        # НОВЫЙ ВОПРОС
        if all_user_cards.count() < 4:
            return redirect('deck_detail', pk=pk)
            
        question_card = random.choice(deck.cards.all())
        wrong_options = all_user_cards.exclude(id=question_card.id).order_by('?')[:3]
        options = list(wrong_options) + [question_card]
        random.shuffle(options)

    return render(request, 'cards/quiz.html', {
        'deck': deck,
        'question_card': question_card,
        'options': options,
        'options_ids': ",".join([str(o.id) for o in options]),
        'status': status,
        'selected_id': selected_id,
        'lives': range(request.session['lives']),
        'score': request.session['score']
    })