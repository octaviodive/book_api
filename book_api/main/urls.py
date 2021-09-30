from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.search_by_id, name='home'),
    path('detail/<str:pk>/', views.details, name='detail'),
    path('csv/<str:pk>', views.csv_file, name='csv_file'),
    path('pdf/<str:pk>', views.pdf_file, name='pdf_file'),    
]
