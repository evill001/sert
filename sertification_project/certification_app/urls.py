from django.urls import path
from . import views
from .views import add_balance, document_list, add_document

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),  
    path('contact/', views.contact, name='contact'),  
    path('onas/', views.onas, name='onas'),  
    path('constructor/', views.constructor, name='constructor'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register_view, name='register'),
    path('add-balance/', views.add_balance, name='add_balance'),
    path('documents/', document_list, name='document_list'),
    path('submit/', views.submit_form, name='submit_form'),
]