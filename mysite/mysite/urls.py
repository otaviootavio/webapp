from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.login_view, name=''),
    path('admin/', admin.site.urls, name='admin'),
    path('olamundo/', views.olamundo, name='olamundo'),
    path('create/base', views.createBase, name='create-base'),
    path('update/base/<str:pk>', views.updateBase, name='update-base'),
    path('update/<str:codigo>', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
    path('flight-data/', views.flightData, name='flight-data'),
    path('crud/', views.crud, name='crud'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login_view'),
    path('monitoracao/', views.monitoracao, name='monitoração'),
    path('monitoracao/update/<str:pk>', views.monitoracao_update, name='monitoração_update'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('relatorios-base/', views.relatoriosBase, name='relatorios-base'),
    path('relatorios-pdf/', views.relatoriosPdf, name='relatorios-pdf'),
    path('logout/', views.logout_view, name='logout_view'),
]
