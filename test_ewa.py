'''
Created on 4 Feb 2023

@author: Famenontsoa
'''
from AmadeusDecoder.utilities.ZenithParser import ZenithParser

if __name__ == '__main__':
    # temp = PdfTextExtractor()
    # attachement_folder = 'test@test.com'
    # file = 'E-ticket 00C948-ABDALLAH DIE .pdf'
    # temp.set_path('EmailFetcher//utilities//attachments_dir//' + attachement_folder + '//' + file)
    # print(temp.get_text_from_pdf())
    temp = ZenithParser()
    attachement_folder = 'test@test.com'
    file = 'Votre reçu pour le dossier 00C6X9.pdf'
    temp.set_path('EmailFetcher//utilities//attachments_dir//' + attachement_folder + '//' + file)
    temp.set_email_date(None)
    temp.set_main_txt_path('EmailFetcher//utilities//attachments_dir//' + attachement_folder + '//' + attachement_folder + '.txt')
    
    content = temp.read_file()
    for line in content:
        print(line)
        
    print('ZENITH', content)
    
    # if not temp.parse_emd(content, temp.get_email_date()):
    # pnr, is_saved = temp.get_pnr_details(content, 'Emis', temp.get_email_date())
    # print(pnr)
    # passengers, pnr_passengers, tickets = temp.get_passengers_tickets(content, pnr)
    # print(passengers, pnr_passengers, tickets)
    #
    # itinerary_part = temp.get_part(content, 'Itinéraire')
    # air_segments = temp.get_itinerary(itinerary_part, pnr)
    # print('Itinéraire', air_segments)
    #
    # cost_details_part = temp.get_part(content, 'Détails du tarif')
    # print('Détails du tarif', cost_details_part)
    # temp.get_ticket_segment_costs(cost_details_part, passengers, air_segments)
    #
    # other_info_part = temp.get_part(content, 'Reçu de paiement')
    # print('Reçu de paiement', other_info_part)
    #
    # ancillaries_info_part = temp.get_part(content, 'Ancillaries')
    # print('Ancillaries', ancillaries_info_part)
    # temp.get_ancillaries_zenith(ancillaries_info_part, pnr, passengers, air_segments)
    
    temp.parse_pnr(temp.get_email_date())
    temp.get_creator_emitter()