'''
Created on 31 Aug 2022

@author: Famenontsoa
'''
import traceback

# from AmadeusDecoder.utilities.ConfigReader import ConfigReader
# ConfigReader.load_company_info()
# ConfigReader.load_email_source()
# ConfigReader.load_emd_parser_tool_data()
# ConfigReader.load_tst_parser_tool_data()
# ConfigReader.load_zenith_parser_tool_data()
# ConfigReader.load_zenith_parser_receipt_tool_data()
# ConfigReader.load_ticket_parser_tool_data()
# ConfigReader.load_fee_request_tool_data()
# ConfigReader.load_report_email_data()
# ConfigReader.load_pnr_parser_tool_data()

from AmadeusDecoder.utilities.AmadeusParser import AmadeusParser

if __name__ == '__main__':
    import os
    
    temp = AmadeusParser() 
    file = '577_issoufali.pnr@gmail.com'
    # file = 12656_famenontsoa@outlook.com'
    temp.set_path(os.getcwd() + '\\EmailFetcher\\utilities\\attachments_dir\\' + file + '\\' + file.removeprefix('VK8PP7_Fixed/') + '.txt')

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
        # if contents[0].startswith('TKT'):
        #     try:
        #         temp.parse_ticket(needed_content, temp.get_email_date())
        #     except:
        #         print('File (Ticket) with error: ' + file)
        #         traceback.print_exc()
        # elif contents[0].startswith('EMD'):
        #     try:
        #         temp.parse_emd(needed_content, temp.get_email_date())
        #     except:
        #         print('File (EMD) with error: ' + file)
        #         traceback.print_exc()
        # elif contents[0].startswith('TST'):
        #     try:
        #         temp.parse_tst(needed_content)
        #     except:
        #         print('File (TST) with error: ' + file)
        #         traceback.print_exc()
        # elif contents[0].startswith('FEE MODIFY REQUEST'):
        #     try:
        #         temp.sf_decrease_request_update(needed_content)
        #     except:
        #         print('File (REQUEST) with error: ' + str(file))
        #         traceback.print_exc()
        if contents[0].startswith('AGY'): # TJQ
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
                if contents[j].startswith('EMD'):
                    try:
                        print('Needed content ', needed_content)
                        print('Needed content 2 ', temp.needed_content(contents[j:]))
                        temp.parse_emd(temp.needed_content(contents[j:]), temp.get_email_date())
                        break
                    except:
                        print('File (EMD) with error: ' + file)
                        traceback.print_exc()
                if contents[j].startswith('TKT'):
                    try:
                        temp.parse_ticket(temp.needed_content(contents[j:]), temp.get_email_date())
                        break
                    except:
                        print('File (Ticket) with error: ' + file)
                        traceback.print_exc()
                if contents[j].startswith('TST'):
                    try:
                        temp.parse_tst(temp.needed_content(contents[j:]), temp.get_email_date())
                        break
                    except:
                        print('File (TST) with error: ' + file)
                        traceback.print_exc()
                if contents[j].startswith('FEE MODIFY REQUEST'):
                    try:
                        temp.sf_decrease_request_update(temp.needed_content(contents[j:]))
                        break
                    except:
                        print('File (REQUEST) with error: ' + file)
                        traceback.print_exc()
                if contents[j].startswith('VOTRE NUMERO DE DOSSIER'):
                    try:
                        needed_content = contents[j:]
                        temp.parse_not_issued_zenith(needed_content)
                        break
                    except:
                        print('File (EWA) with error: ' + file)
                        traceback.print_exc()
