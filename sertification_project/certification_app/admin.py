from django.contrib import admin
from .models import Profile, Document, Application
from decimal import Decimal
from django.core.exceptions import ValidationError

admin.site.register(Profile)
admin.site.register(Document)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "email", "phone")

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username',)

    # Кастомное действие для списания баланса
    def deduct_balance(self, request, queryset):
        for profile in queryset:
            try:
                # Пример: списание фиксированной суммы (можно изменить под запрос)
                amount = Decimal(request.POST.get('deduction_amount', '0'))
                profile.deduct_balance(amount)
                self.message_user(request, f"С баланса {profile.user.username} успешно списано {amount:.2f}")
            except ValidationError as e:
                self.message_user(request, f"Ошибка у {profile.user.username}: {e}", level='error')

    deduct_balance.short_description = "Списать фиксированную сумму с выбранных пользователей"

    # Добавляем действие в админку
    actions = ['deduct_balance']

    # Добавление поля для указания суммы списания
    def get_changelist_form(self, request, **kwargs):
        form = super().get_changelist_form(request, **kwargs)
        form.declared_fields['deduction_amount'] = forms.DecimalField(
            required=False,
            label="Сумма списания",
            min_value=0.01
        )
        return form
    

    class DocumentAdmin(admin.ModelAdmin):
        list_display = ('user', 'title', 'status', 'price')
        search_fields = ('title', 'user__username')
        list_filter = ('status',)