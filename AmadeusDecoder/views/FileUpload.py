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

from django.contrib.auth.decorators import login_required

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
    # Collect all existed PNR in databases 
    pnr_exists = []
    
    # Collect all no founded PNR
    pnr_not_found_set = set()
    
    
    # Match username in csv to existing user in database
    user_match = {
        'Korotimi': 'Koro'
    }
    
    # Collect PNR in uploaded CSV file
    pnr_numbers = []
    
    # Collect unduplicated emitter value in uploaded CSV file
    emitter_criteria_set = set()
    
    # First pass: collect PNR numbers and emitter criteria for batch querying
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        # Use DictReader to read rows as dictionaries
        reader = csv.DictReader(csvfile)
        
        # Iterate each row in reader
        for row in reader:
            try:
                # Parse and clean each field
                pnr_number = row['NPnr'].strip()
                emitter_criteria = row['Emetteur'].strip()

                # print(pnr_number, emitter_criteria)
                
                # Collect PNR numbers and emitter criteria for batch querying ** Ask ChatGPT what is this ?
                pnr_numbers.append(pnr_number)
                filtered_criteria = user_match.get(emitter_criteria, emitter_criteria)
                emitter_criteria_set.add(filtered_criteria.lower())
            except Exception as ex:
                # Log the error without interrupting the flow
                print(f'Error reading row : {row} {ex}')
    
    # Perform batch querying
    pnrs = Pnr.objects.filter(number__in=pnr_numbers, system_creation_date__year__gte=2023).values('number', 'system_creation_date')
    
    user_query = Q()
    for criteria in emitter_criteria_set:
        # The |= operator updates user_query to include the new OR condition. 
        # This means the final user_query will be a combination of all the OR conditions.
        user_query |= Q(username__icontains=criteria) | Q(gds_id__icontains=criteria)
        
    users = User.objects.filter(user_query).values('id', 'username', 'email', 'gds_id')
        
    pnr_dict = {pnr['number']: pnr for pnr in pnrs}
    user_dict = {user['username'].lower(): user for user in users}
    
    # Second pass: process the CSV again to create the final output
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        # Use DictReader to read rows as dictionaries
        reader = csv.DictReader(csvfile)
        
        # Iterate each row in reader
        for row in reader:
            try:
                pnr_number = row['NPnr'].strip()
                emitter_criteria = row['Emetteur'].strip()
                filtered_criteria = user_match.get(emitter_criteria, emitter_criteria).lower()
                
                ticket_issuing_date = datetime.strptime(row['DateEmission'], '%d/%m/%Y').date()    
                ticket_total = float(row['Total'].replace(',', '.'))
                ticket_number = row['Nbillet'].strip()
                
                pnr = pnr_dict.get(pnr_number)
                user = user_dict.get(filtered_criteria)
                
                ticket_emitter = {
                    'username': user['username'] if user else emitter_criteria,
                    'email': user['email'] if user else '',
                }
                
                if pnr is not None:
                    # Append the cleaned data to the final output
                    pnr_exists.append({
                        'pnr': {'number': pnr['number'], 'system_creation_date': pnr['system_creation_date']},
                        'ticket': {
                            'issuing_date': ticket_issuing_date,
                            'total': ticket_total,
                            'number': ticket_number,
                            'emitter': ticket_emitter,
                        },
                    })
                else:
                    pnr_not_found_set.add(pnr_number)
            except Exception as ex:
                # Log the error without interrupting the flow
                print(f'Error reading row with PNR number : {pnr_number} {ex}')
    
    return pnr_exists, pnr_not_found_set


@login_required(login_url='index')
def upload_file(request):
    """
    Handles the file upload and parsing process.

    Args:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The response object.
    """
    from AmadeusDecoder.models.utilities.Refunds import Refunds
    from AmadeusDecoder.models.pnr.Pnr import Pnr
    
    if request.method == 'POST':
        try:
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                # Handle the uploaded file and save it
                file = request.FILES['file_upload']
                file_path = handle_uploaded_file(file)
                # Parse the uploaded CSV file
                pnr_exists, pnr_not_found_set = parse_csv(file_path)
                
                # Convert the set of PNR numbers not found to a list of dictionaries
                pnr_not_found = [{'pnr_number': pnr_number} for pnr_number in pnr_not_found_set]
                
                try:
                    if pnr_exists:
                        refund_objects_to_create = []
                        refund_objects_to_update = []
                        
                        for data in pnr_exists:
                            # Check if a Refunds object with the same number already exists
                            existing_refund = Refunds.objects.filter(number=data['ticket']['number']).first()
                            
                            number = data['ticket']['number']
                            issuing_date = data['ticket']['issuing_date']
                            total = data['ticket']['total']
                            emitter = data['ticket']['emitter']
                            
                            if existing_refund:
                                # Update the existing refund total
                                existing_refund.total = total
                                refund_objects_to_update.append(existing_refund)
                            else:
                                # Create a new refund with all needed info
                                pnr_instance = Pnr.objects.filter(number=data['pnr']['number']).first()
                                if pnr_instance:
                                    refund = Refunds(
                                        pnr=pnr_instance,
                                        number=number,
                                        issuing_date=issuing_date,
                                        total=total,
                                        emitter=emitter,  # Assign emitter field with the dictionary
                                    )
                                    refund_objects_to_create.append(refund)
                                    
                                    
                        '''
                        Key Optimizations:

                        Bulk Create: Using bulk_create to create multiple Refunds objects in a single database hit.
                        Query Filtering: Fetching Pnr and User instances with filter().first() to avoid potential issues if the related objects do not exist.
                        Field Access: Directly accessing the necessary fields from data to populate the Refunds objects.
                        '''
                        
                        # Use bulk_create for efficiency
                        if refund_objects_to_create:
                            Refunds.objects.bulk_create(refund_objects_to_create)
                        
                        # Update existing refunds
                        if refund_objects_to_update:
                            Refunds.objects.bulk_update(refund_objects_to_update, ['total'])

                except Exception as e:
                    print(e)

                # Example: Process parsed_data (save to database, display in template, etc.)
                return JsonResponse({'pnr_exists': pnr_exists, 'pnr_not_found': pnr_not_found}, safe=True)
            else:
                return render(request, 'upload-csv.html', {'form': form})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    # Handle GET request (render the initial form)
    form = UploadFileForm()
    return render(request, 'upload-csv.html', {'form': form})