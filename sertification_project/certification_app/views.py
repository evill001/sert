from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Document, Profile, Application
from .forms import DocumentForm, ApplicationForm


def index(request):
    return render(request, 'index.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')

def onas(request):
    return render(request, 'onas.html')


def constructor(request):
    if request.method == "POST":
        # Получаем данные из формы
        regulation = request.POST.get("regulation")
        product_type = request.POST.get("product_type")
        samples = int(request.POST.get("samples", 1))
        age = request.POST.get("age")
        duration = request.POST.get("duration")
        delivery = request.POST.get("delivery", False)
        translation = request.POST.get("translation", False)
        fast_release = request.POST.get("fast_release", False)

        # Базовая стоимость
        base_price = 10000

        # Логика расчета
        if regulation == "ГОСТ":
            base_price += 5000
        elif regulation == "Технические условия":
            base_price += 3000
        elif regulation == "ИСО":
            base_price += 8000

        if product_type == "Электроника":
            base_price += 4000
        elif product_type == "Игрушки":
            base_price += 2000
        elif product_type == "Медицинская продукция":
            base_price += 7000

        base_price += samples * 500  # Стоимость за каждый образец

        if age == "1-3 года":
            base_price += 2000
        elif age == "Более 3 лет":
            base_price += 5000

        if duration == "6 месяцев":
            base_price += 3000
        elif duration == "1 год":
            base_price += 5000

        if delivery:
            base_price += 2000
        if translation:
            base_price += 3000
        if fast_release:
            base_price += 5000

        # Передаем итоговую стоимость в шаблон
        return render(request, "constructor.html", {"price": base_price})

    return render(request, "constructor.html")


# Форма входа
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Неправильный логин или пароль.')
    return render(request, 'login.html')

# Выход из системы
def logout_view(request):
    logout(request)
    return redirect('index')

# Личный кабинет (профиль пользователя)
@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")

        if password != password_confirm:
            messages.error(request, "Пароли не совпадают!")
            return render(request, "register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Пользователь с таким именем уже существует!")
            return render(request, "register.html")

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Вы успешно зарегистрированы!")
        return redirect("/login/")

    return render(request, "register.html")


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Перенаправляем, если пользователь не авторизован
    
    profile = request.user.profile
    documents = Document.objects.filter(user=request.user)

    context = {
        'profile': profile,
        'documents': documents,
    }
    return render(request, 'profile.html', context)

def add_balance(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount and amount.isdigit():
            profile = request.user.profile
            profile.balance += int(amount)
            profile.save()
    return redirect('profile')


@login_required
def buy_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    profile = request.user.profile

    if profile.balance >= document.price:
        profile.balance -= document.price
        profile.save()
        messages.success(request, f'Вы успешно купили документ "{document.title}" за {document.price} ₽.')
    else:
        messages.error(request, 'Недостаточно средств для покупки этого документа.')

    return redirect('profile')


@login_required
def document_list(request):
    documents = Document.objects.all()
    return render(request, 'document_list.html', {'documents': documents})


def is_admin(user):
    return user.is_staff  # Только администраторы могут добавлять документы

@user_passes_test(is_admin)
def add_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user  # Создатель документа
            document.save()
            messages.success(request, 'Документ успешно добавлен!')
            return redirect('document_list')
    else:
        form = DocumentForm()

    return render(request, 'add_document.html', {'form': form})


def main_page(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "success.html", {"message": "Ваша заявка успешно отправлена!"})
    else:
        form = ApplicationForm()

    return render(request, "main.html", {"form": form})

def contact_page(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "success.html", {"message": "Спасибо за ваше сообщение. Мы свяжемся с вами!"})
    else:
        form = ApplicationForm()

    return render(request, "contact.html", {"form": form})


def submit_form(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Сохранение в базу данных
        Application.objects.create(name=name, phone=phone, email=email, message=message)

        return render(request, "success.html", {"message": "Ваша заявка успешно отправлена!"})
    return render(request, "index.html")