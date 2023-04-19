#coding=utf8
'''
Created on 13 Aug 2021

@author: Famenontsoa
'''

class FileManagement():
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self._path = ''
    
    #getters
    def get_path(self): return self._path
    
    #setters
    def set_path(self, path): self._path = path
    
    ################################# Amadeus text file process #################################
    '''Read a pnr'''
    def readPnrFile(self):
        file = open(self.get_path(), "r+")
        content = file.readlines()
        contents = []
        for line in content:
            contents.append(line.strip())
        return contents
    
    '''Get the pnr issuing date and its number'''
    def getPnrSimpledetail(self):
        from classes.pnr.Pnr import Pnr
        pnr = Pnr()
        fileContent = self.readPnrFile()
        pnrDetailRow = ''
        for i in range(len(fileContent)):
            if(fileContent[i].startswith("RP")):
                pnrDetailRow = fileContent[i]
        pnr.set_number(pnrDetailRow.split(' ')[len(pnrDetailRow.split(' ')) - 1])
        pnr.set_creationdate(pnrDetailRow.split(' ')[len(pnrDetailRow.split(' ')) - 4].split('/')[0])
        pnr.set_exportstatus(0)
        pnr.set_validationstatus(0)
        pnr.set_type('Amadeus')
        pnr.set_agentsignbooking(pnrDetailRow.split('/')[1])
        return pnr
    
    '''Get needed content'''
    def neededContent(self):
        fileContent = self.readPnrFile()
        neededContent = []
        for a in range(len(fileContent)):
            if(fileContent[a].startswith("â€¢") == False and fileContent[a].startswith("•") == False):
                if((fileContent[a].startswith(")>") or fileContent[a].startswith(">")) and a > 0):
                    break
                neededContent.append(fileContent[a])     
        return neededContent
    
    '''Check if regular pnr line: a regular one always start with a number followed by a blank space or a full stop'''
    def isRegularLine(self, line):
        regular = True
        if(line.split(".")[0].isnumeric() == False):
            if(line.split(" ")[0].isnumeric() == False):
                regular = False
        return regular
    
    '''Get normal file without irregular line breaks'''
    def normalizeFile(self):
        actualFileContent = self.neededContent()
        newContent = []
        for i in range(len(actualFileContent)):
            if(self.isRegularLine(actualFileContent[i])):
                newContent.append(actualFileContent[i])
            elif(self.isRegularLine(actualFileContent[i]) == False and len(newContent) > 0):
                newContent[len(newContent) - 1] = newContent[len(newContent) - 1] + " " + actualFileContent[i]
        return newContent
    
    '''Get passengers'''
    def getPassengers(self, pnrcontent):
        from classes.pnrelements.Passenger import Passenger
        passengerline = []
        passengers = []
        # fetch all lines containing passengers
        for i in range(len(pnrcontent)):
            # if all passengers are on the same line
            if(len(pnrcontent[i].split("   ")) > 1 and pnrcontent[i].split(".")[0].isnumeric()):
                passengersOnTheSameLine = pnrcontent[i].split("   ")
                for temp in passengersOnTheSameLine:
                    passengerline.append(temp.split(".")[1])
            # if passengers are on different lines
            else:
                if(pnrcontent[i].split(".")[0].isnumeric()):
                    passengerline.append(pnrcontent[i].split(".")[1])
        
        for line in passengerline:
            temp_passenger = Passenger()
            # if the passenger is a child
            if(len(line.split("(")) > 1): #child
                namepart = line.split("(")[0]
                temp_passenger.set_name(namepart.split("/")[0])
                temp_passenger.set_surname(namepart.split("/")[1])
                designationpart = line.split("(")[1]
                temp_passenger.set_designation(designationpart.split("/")[0])
                temp_passenger.set_birthdate(designationpart.split("/")[1].split(")")[0])
            # if the passenger is not a child
            else:
                namepart = line
                temp_passenger.set_name(namepart.split("/")[0]) 
                surname = ''
                for i in range(len(namepart.split("/")[1].split(" "))):
                    if(namepart.split("/")[1].split(" ")[i] != 'MR' and namepart.split("/")[1].split(" ")[i] != 'MRS'):
                        surname += namepart.split("/")[1].split(" ")[i] + " "
                temp_passenger.set_surname(surname)
                if(len(namepart.split("/")[1].split(" ")[len(namepart.split("/")[1].split(" ")) - 1]) < 4): #check if there is a designation or not
                    temp_passenger.set_designation(namepart.split("/")[1].split(" ")[len(namepart.split("/")[1].split(" ")) - 1])
                else:
                    temp_passenger.set_designation(' ')
            passengers.append(temp_passenger)
        
        return passengers
    
    '''get all flight segments'''
    def getFlight(self, pnrcontent, pnr):
        from classes.pnr.PnrAirSegments import PnrAirSegments
        yearOfOperation = pnr.get_creationdate()[len(pnr.get_creationdate()) - 2: len(pnr.get_creationdate())]
        
        all_flight_lines = []
        flights = []
        
        for line in pnrcontent:
            if(len(line.split(" ")) > 1 and line.split(" ")[0].isnumeric() == True):
                if(line.split(" ")[1] == ''): # because flight line always start with the line number followed by a space
                    all_flight_lines.append(line)
                    
        for flight in all_flight_lines:
            flight_info = flight.split(" ")
            temp_flight = PnrAirSegments()
            # if airline code and flight number are separated with space
            # eg: AF 234, SA 223
            if(len(flight.split(" ")[2]) <= 2):
                airline_code = flight_info[2]
                flight_number = flight_info[3]
                flight_class = flight_info[4]
                departure_airport = flight_info[7][0:3]
                landing_airport = flight_info[7][3:]
                if(flight_info[len(flight_info) - 1] == 'FLWN'):
                    departure_time = flight_info[5] + str(yearOfOperation) + ' ' + '00:00:00'
                    landing_time = None
                else:
                    # to loop the line from the last
                    index = len(flight_info) - 1
                    a = index
                    departure = ''
                    landing = ''
                    if(flight_info[a].startswith('*') or flight_info[a].endswith('*')):
                        while True:
                            if(flight_info[a - 1] != ''):
                                departure = flight_info[a - 2]
                                landing = flight_info[a - 1]
                                break
                            a -= 1
                    else:
                        departure = flight_info[a - 1]
                        landing = flight_info[a]
                    departure_time = flight_info[5] + str(yearOfOperation) + ' ' + departure[0:2] + ':' + departure[2:] + ':00'
                    # sometimes, landing time has a '+' attribute in order to show that some days has to be added from the departure date
                    if(len(landing.split('+')) <= 1):
                        landing_time = flight_info[5] + str(yearOfOperation) + ' ' + landing[0:2] + ':' + landing[2:] + ':00'
                    else:
                        newlandingdate = str(int(flight_info[5][0:2]) + int(landing.split('+')[1])) + flight_info[5][2:]
                        landing_time = newlandingdate + str(yearOfOperation) + ' ' + landing.split('+')[0][0:2] + ':' + landing.split('+')[0][2:] + ':00'
            # if airline code and flight number are not separated with space
            # eg: AF6234, SA1223
            if(len(flight.split(" ")[2]) > 2):
                airline_code = flight_info[2][0:2]
                flight_number = flight_info[2][2:]
                flight_class = flight_info[3]
                departure_airport = flight_info[6][0:3]
                landing_airport = flight_info[6][3:]
                if(flight_info[len(flight_info) - 1] == 'FLWN'):
                    departure_time = flight_info[4] + str(yearOfOperation) + ' ' + '00:00:00'
                    landing_time = None
                else:
                    # to loop the line from the last
                    index = len(flight_info) - 1
                    a = index
                    departure = ''
                    landing = ''
                    if(flight_info[a].startswith('*') or flight_info[a].endswith('*')):
                        while True:
                            if(flight_info[a - 1] != ''):
                                departure = flight_info[a - 2]
                                landing = flight_info[a - 1]
                                break
                            a -= 1
                    else:
                        departure = flight_info[a - 1]
                        landing = flight_info[a]
                    departure_time = flight_info[4] + str(yearOfOperation) + ' ' + departure[0:2] + ':' + departure[2:] + ':00'
                    # sometimes, landing time has a '+' attribute in order to show that some days has to be added from the departure date
                    if(len(landing.split('+')) <= 1):
                        landing_time = flight_info[4] + str(yearOfOperation) + ' ' + landing[0:2] + ':' + landing[2:] + ':00'
                    else:
                        newlandingdate = str(int(flight_info[4][0:2]) + int(landing.split('+')[1])) + flight_info[4][2:]
                        landing_time = newlandingdate + str(yearOfOperation) + ' ' + landing.split('+')[0][0:2] + ':' + landing.split('+')[0][2:] + ':00'
            
            temp_flight.pnrid = pnr.get_id()
            temp_flight.servicecarrier = airline_code
            temp_flight.flightno = flight_number
            temp_flight.codeorg = departure_airport
            temp_flight.codedest = landing_airport
            temp_flight.amanameorg = ''
            temp_flight.amanamedest = ''
            temp_flight.departuretime = departure_time
            temp_flight.arrivaltime = landing_time
            flights.append(temp_flight)
                        
        return flights, flight_class
    
    '''Fetch all contacts on a pnr'''
    def getContacts(self, pnrcontent):
        from classes.pnr.Contact import Contact
        contacts = []
        all_contact_lines = []
        
        for content in pnrcontent:
            if(len(content.split(" ")) > 1 and content.split(" ")[0].isnumeric() == True):
                # all phone contacts and email
                if(content.split(" ")[1] == 'AP' or content.split(" ")[1] == 'APE'):
                    all_contact_lines.append(content)
        
        for line in all_contact_lines:
            temp_contact = Contact()
            if(line.split(" ")[1] == 'AP'):
                temp_contact.set_contacttype('Phone')
                value = ''
                index = 3
                while True:
                    if(index < len(line.split(" "))):
                        value = value + line.split(" ")[index]
                        index += 1
                        if(index >= len(line.split(" ")) or line.split(" ")[index] == '-'):
                                break
                temp_contact.set_value(value)
                owner = None
                if(line.split(" ")[2] == 'PSGR'):
                    owner = 'Passenger'
                elif(len(line.split("-")) > 1):
                    owner = line.split("-")[1].strip()
                temp_contact.set_owner(owner)
            elif(line.split(" ")[1] == 'APE'):
                temp_contact.set_contacttype('Email')
                temp_contact.set_value(line.split(" ")[2])
                temp_contact.set_owner(None)
            contacts.append(temp_contact)
        
        return contacts
                    
        
        for i in range(len(pnrcontent)):
            if(len(pnrcontent[i].split(" ")) > 1 and pnrcontent[i].split(" ")[0].isnumeric() == True):
                '''Fetch all phone contacts'''
                tempcontact = Contact()
                if(pnrcontent[i].split(" ")[1] == 'AP'):
                    tempcontact.set_contacttype('Phone')
                    value = ''
                    index = 3
                    while True:
                        if(index < len(pnrcontent[i].split(" "))):
                            value = value + pnrcontent[i].split(" ")[index]
                            index += 1
                            if(index >= len(pnrcontent[i].split(" ")) or pnrcontent[i].split(" ")[index] == '-'):
                                break
                    tempcontact.set_value(value)
                    owner = ''
                    if(pnrcontent[i].split(" ")[2] == 'PSGR'):
                        owner = 'Passenger'
                    elif(len(pnrcontent[i].split("-")) > 1):
                        owner = pnrcontent[i].split("-")[1].strip()
                    tempcontact.set_owner(owner)
                    '''Fetch all email contacts'''
                elif(pnrcontent[i].split(" ")[1] == 'APE'):
                    tempcontact.set_contacttype('Email')
                    tempcontact.set_value(pnrcontent[i].split(" ")[2])
                    tempcontact.set_owner(None)
                contacts.append(tempcontact)
                
        return contacts
    
    ################################# Amadeus text file process #################################   
    
    '''Listing of all files inside the base directory'''
    @staticmethod
    def fileListing():
        import os
        
        content = {}
        files = []
        from classes.config.Configuration import Configuration
        try:
            configs = Configuration().getBaseFolderConfig("baseFolderAmadeus")[0]
            content['path'] = configs.value
            
            for tempfile in os.listdir(content['path']):
                if(len(tempfile.split('.')) > 1):
                    if(tempfile.split('.')[1] == 'txt'):
                        files.append(content['path'] + '//' + tempfile)
        except Exception as e:
            raise e
        
        return files
    
    '''Listing of all xml or text files inside the Amadeus directory'''
    @staticmethod
    def xmlAmadeusListing(file_type):
        import os
        content = {}
        files = []
        try:
            from utilities.path import pnrXml_path
            configs  = pnrXml_path('')
            content['path'] = configs
            #print(configs)
            #from classes.config.Configuration import Configuration
            #configs = Configuration().getBaseFolderConfig("baseFolderAmadeus")[0]
            #content['path'] = configs.value
            
            for tempfile in os.listdir(content['path']):
                if(len(tempfile.split('.')) > 1):
                    if(tempfile.split('.')[1] == file_type):
                        files.append(content['path'] + '//' + tempfile)
        except Exception as e:
            raise e
        
        return files
#FileManagement.fileListing()
'''pnrnormalized = FileManagement().getPassengers()
for temp in pnrnormalized:
    print("Name: " + temp.get_name() + " ,Surname: " + temp.get_surname() + " ,Designation: " + temp.get_designation()
          + " ,Birthdate: " + str(temp.get_birthdate()))

pnrflights = FileManagement().getFlight()
for temp in pnrflights:
    print(temp.get_departuretime())
    print(temp.get_landingtime())
    
pnrs = FileManagement().normalizeFile()
for temp in pnrs:
    print(temp)
    1

contacts = FileManagement().getContacts()
for temp in contacts:
    print(temp.get_contacttype())
    print(temp.get_value())
    print(temp.get_owner())

print("Pnr detail row")
print(FileManagement().getPnrSimpledetail().get_exportstatus())'''