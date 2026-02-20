from django import forms
from .models import Card

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        # Указываем, какие поля мы хотим видеть в форме
        # Мы НЕ указываем 'deck', потому что будем привязывать карту автоматически
        fields = ['term', 'gender', 'translation', 'image', 'pdf_file']
        labels = {
            'term': 'Wort / Begriff (Слово)',
            'gender': 'Artikel (Артикль)',
            'translation': 'Übersetzung (Перевод)',
            'image': 'Bild (Картинка)',
            'pdf_file': 'PDF-Dokument'
        }
widgets = {
            'term': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'z.B. der Tisch'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'translation': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Например: Стол'}),
        }