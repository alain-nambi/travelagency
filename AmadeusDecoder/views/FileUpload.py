import csv
from datetime import datetime, date
import json
import os
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.utils import timezone

from ..forms import UploadFileForm

from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.user.Users import User
from AmadeusDecoder.models.utilities.Refunds import Refunds
from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.invoice.Ticket import Ticket
from AmadeusDecoder.models.invoice.Fee import OthersFee
from AmadeusDecoder.models.pnr.PnrPassenger import PnrPassenger
from AmadeusDecoder.models.pnr.Passenger import Passenger

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
import logging
from django.db import IntegrityError

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

# Parse issung date
def parse_date(date_str):
    return datetime.strptime(date_str.split()[0], '%d/%m/%Y').date()

# Parse CSV data with specified path folder
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
    pnr_not_found_list = []
    
    occurence_ticket_refund_existing = {
        'exist': 0,
        'not_exist': 0
    }
    
    
    # Match username in csv to existing user in database
    user_match = {
        'Korotimi': 'Koro',
        'Tafara': 'Fouadi',
        'SI': 'Sity',
        'MZE': 'Anaissa'
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
        
    users = User.objects.filter(user_query).values('username', 'email', 'gds_id')
        
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
                issuing_date = row['DateEmission']
                
                ticket_issuing_date = parse_date(issuing_date)
                ticket_total = float(row['Total'].replace(',', '.'))
                ticket_number = row['Nbillet'].strip()
                
                passenger = row['Client'].strip()
                
                pnr = pnr_dict.get(pnr_number)
                user = user_dict.get(filtered_criteria)
                
                ticket_emitter = {
                    'username': user['username'] if user else emitter_criteria,
                    'email': user['email'] if user else '',
                }
                
                if pnr is not None:
                    # Determine if the ticket refund exists
                    existing_ticket_refund = check_ticket_refund_exists(ticket_number)
                    
                    if existing_ticket_refund:
                        occurence_ticket_refund_existing['exist'] += 1
                    else:
                        occurence_ticket_refund_existing['not_exist'] += 1
                    
                    # Append the cleaned data to the final output
                    pnr_exists.append({
                        'pnr': {'number': pnr['number'], 'system_creation_date': pnr['system_creation_date']},
                        'ticket': {
                            'issuing_date': ticket_issuing_date,
                            'total': ticket_total,
                            'number': ticket_number,
                            'emitter': ticket_emitter,
                            'is_ticket_refund_exist': True if existing_ticket_refund else False
                        },
                    })
                else:
                    # Update pnr_not_found_list
                    pnr_not_found_list.append({
                        'pnr': {'number': pnr_number},
                        'ticket': {
                            'issuing_date': ticket_issuing_date,
                            'total': ticket_total,
                            'number': ticket_number,
                            'emitter': ticket_emitter,
                        },
                        'passenger': passenger
                    })
            except Exception as ex:
                # Log the error without interrupting the flow
                print(f'Error reading row with PNR number : {pnr_number} {ex}')
        
        # print('PNRs found:', pnr_not_found_list)
    
    return pnr_exists, pnr_not_found_list, occurence_ticket_refund_existing

# Check if a ticket refund exists
def check_ticket_refund_exists(number):
    # Replace this with your actual logic to check if the ticket refund exists
    return OthersFee.objects.filter(designation=number).exists() 

def user_filter_query(emitter_criteria):
    # The |= operator updates user_query to include the new OR condition. 
    # This means the final user_query will be a combination of all the OR conditions.
    user_query = Q(username__icontains=emitter_criteria) | Q(gds_id__icontains=emitter_criteria)
    return user_query

@login_required(login_url='index')
def upload_file(request):
    """
    Handles the file upload and parsing process.

    Args:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The response object.
    """
    
    if request.method == 'POST':
        try:
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                # Handle the uploaded file and save it
                file = request.FILES['file_upload']
                file_path = handle_uploaded_file(file)
                # Parse the uploaded CSV file
                pnr_exists, pnr_not_found_list, occurence_ticket_refund_existing = parse_csv(file_path)

                # Configure logging
                logging.basicConfig(level=logging.INFO)
                logger = logging.getLogger(__name__)

                # Create PNR and Passenger if pnr is not found
                def create_pnr_and_passenger(pnr_not_found_list):
                    if not pnr_not_found_list:
                        return

                    # Check if PNR is already exist
                    def is_pnr_exist(number):
                        try:
                            pnr = Pnr.objects.filter(number=number).first()
                            logger.info(f'__Checking if PNR exists: {pnr}')
                            if pnr:
                                pnr.system_creation_date = timezone.now()
                                pnr.save()
                                return True
                            return False
                        except Exception as e:
                            logger.error(f"Error checking PNR existence: {number} <> {e}")
                            return False

                    # Create a data set or update pnr data if exist
                    def set_pnr_data(number, agent):
                        try:
                            pnr, created = Pnr.objects.update_or_create(
                                number=number,
                                pnr_status=1,
                                defaults={
                                    'type': 'EWA' if number.startswith('00') else 'Altea',
                                    'agent': agent,
                                    'state': 0,
                                    'status': 'Emis',
                                    'status_value': 0,
                                    'system_creation_date': timezone.now()
                                }
                            )
                            logger.info(f'__PNR {"created" if created else "updated"}: {number}')
                            return pnr
                        except IntegrityError as e:
                            logger.error(f"IntegrityError: {e}")
                            return None

                    # Set passenger informations
                    def set_passenger_data(name):
                        return Passenger(
                            name=name.upper(),
                            order='P1',
                            passenger_status=1,
                        )

                    # Collect PNR and Passenger list to create
                    pnr_to_create_list = []
                    passenger_to_create_list = []

                    for data in pnr_not_found_list:
                        number = data['pnr']['number']
                        emitter = data['ticket']['emitter']['username']
                        agent = User.objects.filter(user_filter_query(emitter)).first()
                        passenger_name = data['passenger']

                        pnr = set_pnr_data(number=number, agent=agent)
                        if pnr:
                            passenger = set_passenger_data(name=passenger_name)
                            if not is_pnr_exist(number=number):
                                pnr_to_create_list.append(pnr)
                                passenger_to_create_list.append(passenger)

                    # Multiple creation to hit database once for performance
                    if pnr_to_create_list:
                        Pnr.objects.bulk_create(pnr_to_create_list)
                        logger.info(f'Bulk created PNRs: {pnr_to_create_list}')
                    if passenger_to_create_list:
                        Passenger.objects.bulk_create(passenger_to_create_list)
                        logger.info(f'Bulk created Passengers: {passenger_to_create_list}')

                    # Collect PNR numbers and Passenger names in list
                    pnr_numbers = [pnr.number for pnr in pnr_to_create_list]
                    passenger_names = [passenger.name for passenger in passenger_to_create_list]

                    # Collect saved PNR and saved Passengers
                    saved_pnrs = {pnr.number: pnr for pnr in Pnr.objects.filter(number__in=pnr_numbers)}
                    saved_passengers = {passenger.name: passenger for passenger in Passenger.objects.filter(name__in=passenger_names)}

                    pnr_passenger_list = []

                    # Zip pnr and passenger list to make update of pnr passengers table
                    for pnr, passenger in zip(pnr_to_create_list, passenger_to_create_list):
                        saved_pnr = saved_pnrs[pnr.number]
                        saved_passenger = saved_passengers[passenger.name]
                        pnr_passenger = PnrPassenger(
                            pnr=saved_pnr,
                            passenger=saved_passenger
                        )
                        pnr_passenger_list.append(pnr_passenger)

                    if pnr_passenger_list:
                        PnrPassenger.objects.bulk_create(pnr_passenger_list)
                        logger.info(f'Bulk created PnrPassenger relationships: {pnr_passenger_list}')

                try:
                    create_pnr_and_passenger(pnr_not_found_list)
                except Exception as e:
                    logger.error(f"An error occurred: {e}")
                
                
                try:
                    # Check if there are any PNRs that exist in the system.
                    if pnr_exists:
                        # Initialize lists to collect refund objects to create and update.
                        refund_objects_to_create = []
                        refund_objects_to_update = []

                        # Iterate over each data entry in the existing PNRs.
                        for data in pnr_exists:
                            # Extract ticket information from the data.
                            number = data['ticket']['number']
                            issuing_date = data['ticket']['issuing_date']
                            
                            # Convert issuing_date to aware datetime if naive
                            if isinstance(issuing_date, date) and not isinstance(issuing_date, datetime):
                                # Convert date to datetime
                                issuing_date = datetime.combine(issuing_date, datetime.min.time())
                            if timezone.is_naive(issuing_date):
                                issuing_date = timezone.make_aware(issuing_date, timezone.get_current_timezone())
                            
                            total = data['ticket']['total']
                            emitter = data['ticket']['emitter']
                            
                            # Retrieve the existing refund object with the same ticket number, if it exists.
                            existing_refund = Refunds.objects.filter(number=number).first()
                            
                            # Check if a ticket refund exists for the given ticket number.
                            existing_ticket_refund = check_ticket_refund_exists(number)
                            
                            if existing_refund:
                                # Update the total, emitter, and ticket refund existence flag for the existing refund.
                                existing_refund.total = total
                                existing_refund.emitter = emitter
                                existing_refund.is_ticket_refund_exist = bool(existing_ticket_refund)
                                
                                # Add the existing refund to the list of objects to update.
                                refund_objects_to_update.append(existing_refund)
                                
                                
                                # Update OthersFee object total based on the ticket data.
                                other_fee_instance = OthersFee.objects.filter(designation=number).first()
                                
                                if other_fee_instance:
                                    other_fee_instance.cost = total
                                    other_fee_instance.tax = 0
                                    other_fee_instance.total = total
                                    other_fee_instance.save()
                            else:
                                # Retrieve or create related PNR and User instances based on the ticket data.
                                pnr_instance = Pnr.objects.filter(number=data['pnr']['number']).first()
                                user_instance = User.objects.filter(user_filter_query(emitter['username'])).first()
                                pnr_passenger_instance = PnrPassenger.objects.filter(pnr=pnr_instance).first()

                                if pnr_instance:
                                    refund = Refunds(
                                        pnr=pnr_instance,
                                        number=number,
                                        issuing_date=issuing_date,
                                        total=total,
                                        emitter=emitter,
                                        is_ticket_refund_exist=bool(existing_ticket_refund)
                                    )
                                    
                                    # Add the new refund to the list of objects to create.
                                    refund_objects_to_create.append(refund)                             
                                    
                                    try:
                                        # Check if ticket refund is already exist on other_fee table
                                        other_fee_instance = OthersFee.objects.filter(designation=number).first()

                                        # Create OthersFee object based on the ticket data.
                                        if not other_fee_instance:
                                            other_fee = OthersFee(
                                                designation=number,
                                                cost=total,
                                                tax=0,
                                                total=total,
                                                pnr=pnr_instance,  # Ensure pnr_instance is a Pnr instance
                                                is_subjected_to_fee=False,
                                                fee_type='EMD',
                                                other_fee_status=1,
                                                emitter=user_instance,
                                                passenger=pnr_passenger_instance.passenger if pnr_passenger_instance else None,
                                                creation_date=issuing_date 
                                            )
                                            other_fee.save()
                                    except Exception as e:
                                        # Log the error and stop processing if an exception occurs.
                                        print(f"Error updating or creating refund: {e}")                      
                        
                        # Use bulk_create to efficiently insert multiple refund objects into the database.
                        if refund_objects_to_create:
                            Refunds.objects.bulk_create(refund_objects_to_create)
                        
                        # Use bulk_update to efficiently update multiple refund objects in the database.
                        if refund_objects_to_update:
                            Refunds.objects.bulk_update(refund_objects_to_update, ['total', 'emitter', 'is_ticket_refund_exist'])

                except Exception as e:
                    # Log any exception that occurs in the entire block.
                    print(f"Error : {e}")

                # Return the results in a JSON response.
                return JsonResponse({'pnr_exists': pnr_exists, 'pnr_not_found_list': pnr_not_found_list, 'occurence_ticket_refund_existing': occurence_ticket_refund_existing}, safe=True)

            return render(request, 'upload-csv.html', {'form': form})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    # Handle GET request (render the initial form)
    form = UploadFileForm()
    return render(request, 'upload-csv.html', {'form': form})