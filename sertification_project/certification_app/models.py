from django.db import models
from django.contrib.auth.models import User

# Расширение профиля пользователя
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Баланс пользователя

    def __str__(self):
        return self.user.username

# Модель документа
class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)  # Название документа
    description = models.TextField(blank=True, null=True)  # Описание документа
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=50, 
        choices=[('created', 'Created'), ('completed', 'Completed')], 
        default='created'
    )  # Статус документа
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Цена документа

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