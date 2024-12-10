from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='base'),
    path('index/', views.index, name='index'),
    path('delete-all/', views.delete_all_data, name='delete_all_data'),
    path('import-excel/', views.import_excel, name='import_excel'),
]