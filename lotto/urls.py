from django.urls import path
from . import views

urlpatterns = [
    path('',              views.home,        name='home'),
    path('buy/',          views.buy_ticket,  name='buy_ticket'),
    path('my-tickets/',   views.my_tickets,  name='my_tickets'),
]
