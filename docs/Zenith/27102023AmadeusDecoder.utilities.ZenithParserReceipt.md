# Utilisation d'AmadeusDecoder

Créé par: Alain RAKOTOARIVELO
Heure de création: 18 octobre 2023 08:22
Étiquettes: AmadeusDecoder

### Faire le test avec le PNR Zenith

TESTEWA : 
1. Créer un nouveau dossier test@test.com
2. Créer un fichier test@test.com dans le dossier test@test.com 
3. Insérer le fichier PDF dans le dossier test@test.com
4. Lancer le test avec la commande `python test_ewa.py`

AmadeusDecoder/utilities/ZenithParser.py	
    set_email_date
	get_most_recent_pnr
	read_file
	check_fee_subjection_status
	get_not_emitted_pnr_details
	get_not_emitted_pnr_passengers
	format_date
	get_not_emitted_pnr_itinerary
	get_not_emitted_pnr_opc
	get_not_emitted_pnr_fare
	read_main_text_file
	get_txt_path_from_pdf
	get_creator_emitter
	parse_emd
	get_pnr_details
	clean_content_array
	clean_passenger_type
	clean_ticket_number
	clean_passenger_name
	normalize_passenger_content
	normalize_passenger
	get_passengers_tickets
	get_part
	get_itinerary
	separate_cost_per_passenger_type
	get_ticket_segment_costs
	get_ancillaries_zenith
	process_taxes
	get_other_info
	parse_pnr
	save_data