from django.db import models

# Create your models here.
class PDFUpload(models.Model):
    pdf_file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class PDFPageContent(models.Model):
    pdf = models.ForeignKey(PDFUpload, on_delete=models.CASCADE)
    page_number = models.IntegerField()
    extracted_text = models.TextField()