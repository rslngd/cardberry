from django.db import models
from django.contrib.auth.models import User

# 1. Создаем список вариантов для выбора (хранится в базе : отображается пользователю)
GENDER_CHOICES = [
    ('masc', 'der (Maskulinum - Мужской)'),
    ('fem', 'die (Femininum - Женский)'),
    ('neut', 'das (Neutrum - Средний)'),
    ('', '--- (Kein Artikel/Andere - Нет артикля)'), # Для глаголов, прилагательных и т.д.
]

class Deck(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название колоды")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='cards')
    term = models.CharField(max_length=255, default='', verbose_name="Термин (DE)")
    
    # 2. НОВОЕ ПОЛЕ: Артикль
    gender = models.CharField(
        max_length=4,         # Короткие коды: masc, fem, neut
        choices=GENDER_CHOICES, # Используем наш список
        blank=True,           # Может быть пустым (для глаголов)
        default='',           # По умолчанию пусто
        verbose_name="Артикл (Genus)"
    )
    
    translation = models.CharField(max_length=255, default='', verbose_name="Перевод (RU)")
    image = models.ImageField(upload_to='cards/images/', blank=True, null=True, verbose_name="Изображение")
    pdf_file = models.FileField(upload_to='cards/pdf/', blank=True, null=True, verbose_name="PDF файл")
    
    def __str__(self):
        return f"{self.term} - {self.translation}"