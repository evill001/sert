from django import forms
from .models import Document, Application

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'description', 'price']


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["name", "email", "phone", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ваше имя", "class": "form-control"}),
            "email": forms.EmailInput(attrs={"placeholder": "Ваш email", "class": "form-control"}),
            "phone": forms.TextInput(attrs={"placeholder": "Ваш телефон", "class": "form-control"}),
            "message": forms.Textarea(attrs={"placeholder": "Ваше сообщение", "class": "form-control", "rows": 4}),
        }