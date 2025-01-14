from django.urls import path
from . import views
from .views import add_balance, buy_document, document_list, add_document

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('services/', views.services, name='services'),  # Услуги
    path('contact/', views.contact, name='contact'),  # Контакты
    path('onas/', views.onas, name='onas'),  # О нас
    path('constructor/', views.constructor, name='constructor'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register_view, name='register'),
    path('add-balance/', add_balance, name='add_balance'),
    path('buy-document/<int:document_id>/', buy_document, name='buy_document'),
    path('documents/', document_list, name='document_list'),
    path('submit/', views.submit_form, name='submit_form'),
]