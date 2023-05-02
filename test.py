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
from AmadeusDecoder.models.pnr.Pnr import Pnr
# from AmadeusDecoder.models.invoice.Fee import ReducePnrFeeRequest, Fee
session_variables.current_company = ConfigReader.get_company()

from AmadeusDecoder.utilities.AmadeusParser import AmadeusParser

if __name__ == '__main__':
    import os

    temp = Pnr.objects.filter(id=17263).first()
    temp.delete()