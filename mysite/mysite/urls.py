from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.home, name=''),
    path('admin/', admin.site.urls, name='admin'),
    path('create/base', views.createBase, name='create-base'),
    path('update/base/<str:pk>', views.updateBase, name='update-base'),
    path('delete/base/<str:pk>', views.deleteBase, name='delete-base'),
    path('crud/', views.crud, name='crud'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login_view'),
    path('monitoracao/', views.monitoracao, name='monitoração'),
    path('monitoracao/update/<str:pk>', views.monitoracao_update, name='monitoração_update'),
    path('monitoracao/delete/<str:pk>', views.monitoracao_delete, name='monitoração_delete'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('relatorios-base/', views.relatoriosBase, name='relatorios-base'),
    path('relatorios-pdf/', views.relatoriosPdf, name='relatorios-pdf'),
    path('logout/', views.logout_view, name='logout_view'),
]
