from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.contrib import admin

# Расширение профиля пользователя
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} - {self.balance:.2f}"

    def deduct_balance(self, amount):
        """Списать баланс пользователя."""
        amount = Decimal(amount)
        if amount <= 0:
            raise ValidationError("Сумма списания должна быть больше 0.")
        if self.balance < amount:
            raise ValidationError("Недостаточно средств.")
        self.balance -= amount
        self.save()

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=50, 
        choices=[('created', 'Created'), ('completed', 'Completed')], 
        default='created'
    )
    file = models.FileField(upload_to='documents/', blank=True, null=True)  # Загруженные файлы хранятся в media/documents/

    def __str__(self):
        return self.title

    
class Application(models.Model):
    name = models.CharField("Имя клиента", max_length=100)
    email = models.EmailField("Email клиента")
    phone = models.CharField("Телефон", max_length=20)
    message = models.TextField("Сообщение", blank=True, null=True)
    created_at = models.DateTimeField("Дата и время заявки", auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email} ({self.created_at})"

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"