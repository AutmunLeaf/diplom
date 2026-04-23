from django.urls import path
from . import views

urlpatterns = [
    path('', views.ks2_list, name='ks2_list'),
    path('create/', views.ks2_create, name='ks2_create'),
    path('<int:pk>/edit/', views.ks2_edit, name='ks2_edit'),
    path('<int:pk>/delete/', views.ks2_delete, name='ks2_delete'),
    path('<int:pk>/work/<int:work_pk>/delete/', views.ks2_delete_work, name='ks2_delete_work'),
]
