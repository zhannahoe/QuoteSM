from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('registration', views.registration),
    path('quotes', views.quotes),
    path('login', views.login),
    path('logout', views.logout),
    path('addQuote', views.addQuote),
    path('delete/<int:quoteid>', views.delete),
    path('edit/myaccount/<int:userid>', views.editUserPage),
    path('edit/<int:userid>', views.editUser),
    path('user/<int:userid>', views.users),
    path('likeQuote/<int:quoteid>', views.likeQuote)
]