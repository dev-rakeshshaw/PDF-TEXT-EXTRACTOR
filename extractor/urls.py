from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.upload_pdf, name='upload_pdf'),
    path('pdf_details/', views.pdf_details, name='pdf_details'),
    path('delete_all/', views.delete_all_records, name='delete_all_records'),  # Route for deleting all records
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)