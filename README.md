# PDF Text Extractor

## Overview

The PDF Text Extractor is a Django web application that allows users to upload PDF files and extracts text content from them. The extracted text is then stored in a database, and users can view the extracted content in a tabular format. This application also utilizes threading to ensure that the text extraction process does not block the main application, allowing for a smooth user experience.

## Features

- Upload PDF files.
- Extract text content from each page of the uploaded PDF.
- Store extracted text in a database.
- View extracted content in a table format.
- Option to delete all extracted records.
- Background processing of text extraction using threading.

## Technologies Used

- Python
- Django
- PyPDF2 (for PDF text extraction)
- SQLite (for the database, can be replaced with other database systems)

## Getting Started

### Prerequisites

- Python 3.x
- Django
- PyPDF2
- A web browser

### Installation

1. Clone this repository to your local machine:
   ```bash
   git clone <repository-url>
   cd pdf-text-extractor


python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`


pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
