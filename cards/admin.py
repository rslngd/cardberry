from django.contrib import admin
from .models import Deck, Card # Точка перед models означает "из текущей папки"

admin.site.register(Deck)
admin.site.register(Card)