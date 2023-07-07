from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('<int:id>', views.view_student, name='view_student'),
  path('add/', views.add, name='add'),
  path('edit/<int:id>/', views.edit, name='edit'),
  path('delete/<int:id>/', views.delete, name='delete'),
  path('files/',views.files,name='files'),
  path('automate/<int:id>/', views.automate, name='automate'),
  path('send_files/',views.send_files,name='send_files'),
  path('user_list/', views.user_list, name='user_list'),
  path('user_create/', views.user_create, name='user_create'),
  path('user_delete/<str:pk>/', views.delete_user, name='user_delete'),
  path('user_update/<str:pk>/', views.user_update, name='user_update'),
  path('dashboard/', views.dashboard, name='dashboard'),
]

