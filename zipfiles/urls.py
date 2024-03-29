from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('view_info/<int:id>', views.view_info, name='view_info'),
  path('add/', views.add, name='add'),
  path('edit/<int:id>/', views.edit, name='edit'),
  path('delete/<int:id>/', views.delete, name='delete'),
  path('files/',views.files,name='files'),
  path('report/',views.report,name='report'),
  path('automate/<int:id>/', views.automate, name='automate'),
  path('download_file/<int:id>/', views.download_file, name='download_file'),
  path('automate_all/', views.automate_all, name='automate_all'),
  path('send_files/',views.send_files,name='send_files'),
  path('user_list/', views.user_list, name='user_list'),
  path('user_create/', views.user_create, name='user_create'),
  path('user_delete/<str:pk>/', views.delete_user, name='user_delete'),
  path('user_update/<str:pk>/', views.user_update, name='user_update'),
  path('dashboard/', views.dashboard, name='dashboard'),
  path('delete_all/', views.delete_all, name='delete_all'),
]

