from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('upload', views.upload, name='upload'),
    #path('tickets', views.tickets, name='tickets'),
    #path('ticket', views.ticket, name='ticket'),

]
