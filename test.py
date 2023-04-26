'''
Created on 31 Aug 2022

@author: Famenontsoa
'''
import traceback

# from AmadeusDecoder.utilities.PdfTextExtractor import PdfTextExtractor
# from AmadeusDecoder.utilities.PnrCostParser import PnrCostParser
# from AmadeusDecoder.utilities.TjqOnlyParser import TjqOnlyParser
# from AmadeusDecoder.utilities.TjqMailAlert import alert_tjq
# from AmadeusDecoder.models.pnrelements.PnrAirSegments import PnrAirSegments

# assign current company to local variable 'session_variable'
import AmadeusDecoder.utilities.session_variables as session_variables
from AmadeusDecoder.utilities.ConfigReader import ConfigReader
# from AmadeusDecoder.models.invoice.Fee import ReducePnrFeeRequest, Fee
session_variables.current_company = ConfigReader.get_company()

from AmadeusDecoder.utilities.AmadeusParser import AmadeusParser

if __name__ == '__main__':
    import os
    
    # from AmadeusDecoder.models.pnr.Pnr import Pnr
    # temp_pnr_delete = Pnr.objects.filter(number='OBHOVJ').first()
    # temp_pnr_delete.delete()
    
    temp = AmadeusParser() 
    file = '2_fnd@amadeus.com'
    # file = 12656_famenontsoa@outlook.com'
    temp.set_path(os.getcwd() + '//EmailFetcher//utilities//attachments_dir//' + file + '//' + file.removeprefix('VK8PP7_Fixed/') + '.txt')

    contents = temp.read_file()
    needed_content = temp.needed_content(contents)
    normalize_file = temp.normalize_file(needed_content)

    # alert_tjq()
    
    # <A HREF="mailto:?subject=look at this website&body=Hi, I found this website and thought you might like it http://www.geocities.com/wowhtml/">tell a friend</A>
    
    # for content in normalize_file:
    #     print(content)
    
    # print(needed_content)
    for content in needed_content:
        print(content)
    
    # temp.parse_tst(needed_content)
    # print(temp.get_tst_related_pnr(needed_content))
    temp.set_email_date(None)
    if len(contents) > 0:
        if contents[0].startswith('TKT'):
            try:
                temp.parse_ticket(needed_content, temp.get_email_date())
            except:
                print('File (Ticket) with error: ' + file)
                traceback.print_exc()
        elif contents[0].startswith('EMD'):
            try:
                temp.parse_emd(needed_content, temp.get_email_date())
            except:
                print('File (EMD) with error: ' + file)
                traceback.print_exc()
        elif contents[0].startswith('TST'):
            try:
                temp.parse_tst(needed_content)
            except:
                print('File (TST) with error: ' + file)
                traceback.print_exc()
        elif contents[0].startswith('FEE MODIFY REQUEST'):
            try:
                temp.sf_decrease_request_update(needed_content)
            except:
                print('File (REQUEST) with error: ' + str(file))
                traceback.print_exc()
        elif contents[0].startswith('AGY'): # TJQ
            try:
                temp.parse_tjq(needed_content)
            except:
                print('File (TJQ) with error: ' + str(file))
                traceback.print_exc()
        else:
            for j in range(len(contents)):
                if contents[j].startswith('RPP'):
                    temp.set_is_archived(True)
                    continue
                if contents[j].startswith('RP') and not contents[j].startswith('RPP'):
                    try:
                        temp.parse_pnr(contents[j:], needed_content, temp.get_email_date())
                        break
                    except:
                        print('File (PNR) with error: ' + file)
                        traceback.print_exc()
                if contents[j].startswith('VOTRE NUMERO DE DOSSIER'):
                    try:
                        needed_content = contents[j:]
                        temp.parse_not_issued_zenith(needed_content)
                        break
                    except:
                        print('File (EWA) with error: ' + file)
                        traceback.print_exc()
                if contents[j].startswith('FEE MODIFY REQUEST'):
                    try:
                        temp.sf_decrease_request_update(needed_content)
                        break
                    except:
                        print('File (FEE MODIFY REQUEST) with error: ' + str(file))
                        traceback.print_exc()
    # get_segment_by_ticket(65)
    
    # from AmadeusDecoder.models.invoice.Ticket import Ticket
    # from AmadeusDecoder.models.invoice.TicketPassengerSegment import TicketPassengerSegment
    # ticket  = Ticket.objects.filter(number = '7609010406267').first()
    # print(ticket)
    # segments = ticket.ticket_parts.all()
    # print(segments[0].segment.codeorg.iata_code)
    
    # import AmadeusDecoder.utilities.session_variables as session_variables
    # from AmadeusDecoder.utilities.ConfigReader import ConfigReader
    # session_variables.current_company = ConfigReader.get_company()
    

'''
if __name__ == "__main__":
    # all_available_reduce_fee_request = ReducePnrFeeRequest.objects.filter(status=0).all()
    # header = 'Numéro du PNR;Premier Passager;Montant original du fee;Montant demandé;Numéro du billet;Montant du billet;Nom du demandeur'
    # content = []
    # no_response = ['TT6PUG']
    # denied = ['VIY8R6']
    # for reduce_fee in all_available_reduce_fee_request:
    #     pnr = reduce_fee.pnr
    #     fee = reduce_fee.fee
    #     ticket = fee.ticket
    #
    #     pnr_number = pnr.number
    #     first_passenger = pnr.passengers.first().passenger
    #     origin_amount = reduce_fee.origin_amount
    #     requested_amount = reduce_fee.amount
    #     ticket_number = ticket.number
    #     ticket_fare = ticket.total
    #     request_user = reduce_fee.user
    #
    #     line = {'pnr_number': pnr_number, 'first_passenger':first_passenger, 'origin_amount':origin_amount, 
    #             'requested_amount':requested_amount, 'ticket_number':ticket_number, 'ticket_fare':ticket_fare, 
    #             'request_user':request_user}
    #     content.append(line)
    #
    #     if pnr.number in denied:
    #         reduce_fee.status = 2
    #         reduce_fee.save()
    #     elif pnr.number not in denied and pnr_number not in no_response:
    #         reduce_fee.status = 1
    #         reduce_fee.save()
    #
    #         fee.cost = requested_amount
    #         fee.total = requested_amount
    #         fee.save()
    #
    # with(open('request.csv', 'a') as file):
    #     file.write(header)
    #     for one_line in content:
    #         file.write(one_line['pnr_number']+';'+
    #                     one_line['first_passenger']+';'+ 
    #                     one_line['origin_amount']+';'+
    #                     one_line['requested_amount']+';'+
    #                     one_line['ticket_number']+';'+
    #                     one_line['ticket_fare']+';'+
    #                     one_line['request_user'])
    all_accepted_reduce_request = ReducePnrFeeRequest.objects.filter(status=1).all()
    for reduce_request in all_accepted_reduce_request:
        fee = reduce_request.fee
        fee.cost = reduce_request.amount
        fee.total = reduce_request.amount
        fee.save()
'''
