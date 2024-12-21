from django.urls import path
from .views import upload_pdf, index, get_job_trends, get_recommendations

urlpatterns = [
    path('upload/', upload_pdf, name='upload_pdf'),
    path('', index, name='index.html'),
    path('trends/', get_job_trends, name='job_trends'),
    path('recommendations/', get_recommendations, name='recommendations'),
]