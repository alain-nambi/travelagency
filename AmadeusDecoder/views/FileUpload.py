import csv
from datetime import datetime
import os
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings

from AmadeusDecoder.models.pnr.Pnr import Pnr
from ..forms import UploadFileForm
from AmadeusDecoder.models.user.Users import User

def handle_uploaded_file(f):
    """
    Handles the uploaded file by saving it to the specified directory.

    Args:
    - f (UploadedFile): The uploaded file object.

    Returns:
    - str: The path to the saved file.
    """
    # Define the directory where you want to save uploaded files
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Create the full file path
    file_path = os.path.join(upload_dir, f.name)
    
    # Save the uploaded file to the filesystem
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    return file_path

def parse_csv(file_path):
    """
    Parses the CSV file at the given file path and extracts relevant data.

    Args:
    - file_path (str): The path to the CSV file to be parsed.

    Returns:
    - list of dict: A list of dictionaries containing the parsed data.
    """
    data = []

    # Open the CSV file for reading
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)  # Use DictReader to read rows as dictionaries

        user_match = {
            'Korotimi': 'Koro'
        }
        
        for row in reader:
            try:
                # Parse and clean each field
                issuing_date = datetime.strptime(row['DateEmission'], '%d/%m/%Y').date()
                pnr_number = row['NPnr'].strip()
                total = float(row['Total'].replace(',', '.'))
                ticket_number = row['Nbillet'].strip()

                # Get emitter criteria and find the user
                emitter_criteria = row['Emetteur'].strip()
                
                # Use the mapping dictionary to get the correct criteria for filtering
                filter_criteria = user_match.get(emitter_criteria, emitter_criteria)
                
                pnr = Pnr.objects.filter(number__icontains=pnr_number).first()
                user = User.objects.filter(Q(username__icontains=filter_criteria.lower()) | Q(gds_id__icontains=filter_criteria.lower())).first()

                # Prepare the emitter dictionary
                emitter = {
                    'id': user.id if user else '',
                    'username': user.username if user else emitter_criteria,
                    'email': user.email if user else ''
                }

                # Append the cleaned and parsed data to the list
                data.append({
                    'issuing_date': issuing_date,    # Date when the ticket was issued
                    'pnr_number': pnr_number,       # Passenger Name Record number
                    'total': total,                 # Total amount
                    'ticket_number': ticket_number, # Ticket number
                    'emitter': emitter,             # Emitter information
                    'emitter_criteria': filter_criteria,  # Emitter criteria for matching
                    'is_exist': pnr
                })

            except Exception as ex:
                # Print an error message if parsing fails for a row
                print(f"Error parsing pnr number: {pnr_number}: {ex}")

    return data

def upload_file(request):
    """
    Handles the file upload and parsing process.

    Args:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The response object.
    """
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle the uploaded file and save it
            file_path = handle_uploaded_file(request.FILES['file'])
            # Parse the uploaded CSV file
            parsed_data = parse_csv(file_path)

            # Example: Process parsed_data (save to database, display in template, etc.)
            return JsonResponse({'parsed_data': parsed_data}, safe=True)
            
            # Uncomment the next line to redirect to a success page after processing
            # return HttpResponseRedirect('/success/')
    else:
        form = UploadFileForm()
    
    return render(request, 'upload.html', {'form': form})