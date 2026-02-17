from django.db import models
from django.contrib.auth.models import User

class Deck(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название колоды")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='cards')
    term = models.CharField(max_length=255, verbose_name="Термин (DE/EN)")
    translation = models.CharField(max_length=255, verbose_name="Перевод (RU)")
    
    # Новые поля для медиа
    image = models.ImageField(upload_to='cards/images/', blank=True, null=True, verbose_name="Изображение")
    pdf_file = models.FileField(upload_to='cards/pdf/', blank=True, null=True, verbose_name="PDF файл")
    
    def __str__(self):
        return f"{self.term} - {self.translation}"