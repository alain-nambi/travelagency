'''
Created on Jul 13, 2023

@author: Famenontsoa
'''

class Utility():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    # separate number from string
    @staticmethod
    def separate_number(target_string, number_size_constraint=13):
        separated_tokens = []
        fetched_number = []
        previous_token = ''
        current_number = ''
        for i in range(len(target_string)):
            if i > 0:
                previous_token = target_string[i-1]
            
            if target_string[i].isnumeric():
                if previous_token.isnumeric():
                    current_number += target_string[i]
                else:
                    current_number = target_string[i]
            else:
                if current_number.isnumeric():
                    if len(current_number) == number_size_constraint:
                        fetched_number.append(current_number)
                    current_number = ''
            
            if current_number.isnumeric() and i == len(target_string) - 1 and len(current_number) == number_size_constraint:
                fetched_number.append(current_number)
                
        for number in fetched_number:
            target_string_split = target_string.split(number)
            for i in range(len(target_string_split)):
                if target_string_split[i] not in separated_tokens and target_string_split[i] != '':
                    separated_tokens.append(target_string_split[i])
                    if i < len(target_string_split) - 1:
                        separated_tokens.append(number)
        
        if len(fetched_number) > 0:
            if target_string[0:number_size_constraint] in fetched_number:
                separated_tokens.insert(0, target_string[0:number_size_constraint])
        
        return separated_tokens
    