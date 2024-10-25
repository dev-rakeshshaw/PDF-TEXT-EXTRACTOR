# extractor/views.py
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .models import PDFUpload, PDFPageContent
from PyPDF2 import PdfReader
from django.shortcuts import render, get_object_or_404
from .models import PDFUpload, PDFPageContent
import threading
from django.shortcuts import redirect


def extract_pdf_text(pdf_file_path, pdf_upload_id):
    """
    Extracts text from the PDF file located at the given file path.

    This function opens the specified PDF file in binary read mode, 
    reads each page, extracts the text content, and saves it to the 
    PDFPageContent model. The function is intended to be run in a 
    separate thread to prevent blocking the main thread, allowing 
    the web application to remain responsive while text extraction 
    is in progress.

    Args:
        pdf_file_path (str): The filesystem path to the PDF file 
                             from which text is to be extracted.
        pdf_upload_id (int): The ID of the PDFUpload instance associated 
                             with this PDF file, used to link extracted 
                             text data to the corresponding PDF.

    The function prints a statement indicating the current page being 
    processed and another statement once the text extraction for that 
    page is completed. If no text is found on a page, it stores a 
    placeholder message ("No text found") in the database.
    """
    with open(pdf_file_path, 'rb') as pdf_file:  # Open the file in binary read mode
        pdf_reader = PdfReader(pdf_file)
        for page_num, page in enumerate(pdf_reader.pages):
            print(f"Extracting text from Page {page_num + 1}...")  # Print statement for tracing
            text = page.extract_text()
            content = text if text else "No text found"
            PDFPageContent.objects.create(
                pdf_id=pdf_upload_id,
                page_number=page_num + 1,
                extracted_text=content
            )
            print(f"Text extracted for Page {page_num + 1}: {content[:30]}...")  # Print first 30 characters of extracted text

# Threading is used here------------------->
def upload_pdf(request):
    """
    Handles the upload of a PDF file and initiates text extraction.

    This view checks for a POST request containing a PDF file. Upon 
    receiving a valid file, it saves the file using Django's 
    FileSystemStorage and retrieves the actual filesystem path. 

    A new thread is then started to handle the text extraction 
    process without blocking the main thread, allowing the user to 
    receive a response that the extraction has started.

    Args:
        request (HttpRequest): The HTTP request object containing 
                               the uploaded PDF file.

    Returns:
        HttpResponse: Renders the upload page with a message indicating 
                      that text extraction has started. If the request 
                      method is not POST or no file is provided, it 
                      simply returns the upload page without any message.
    """
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']
        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        uploaded_file_path = fs.path(filename)  # Get the actual filesystem path
        
        # Start a new thread for the text extraction
        thread = threading.Thread(target=extract_pdf_text, args=(uploaded_file_path, PDFUpload.objects.create(pdf_file=pdf_file).id))
        thread.start()

        message = f"Text extraction started for the file: {pdf_file.name}. It will complete in the background."
        return render(request, 'extractor/upload.html', {'message': message})

    return render(request, 'extractor/upload.html')


def pdf_details(request):
    """
    Displays a table of all extracted content from the database.

    This view retrieves all records from the PDFPageContent model, 
    sorted by the associated PDF and page number, and renders them 
    in a tabular format for the user to view.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the pdf_details template with the 
                      extracted content data.
    """
    # Fetch all records from the PDFPageContent table
    extracted_data = PDFPageContent.objects.all().order_by('pdf', 'page_number')

    return render(request, 'extractor/pdf_details.html', {
        'extracted_data': extracted_data,
    })


def delete_all_records(request):
    """
    Deletes all records from the PDFPageContent model.

    This view allows the user to clear all extracted text data 
    from the database, effectively resetting the content.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the pdf_details page after 
                      clearing the records.
    """
    # Delete all records in the PDFPageContent table
    PDFPageContent.objects.all().delete()
    
    # Redirect back to the pdf_details page (which will now be empty)
    return redirect('pdf_details')
