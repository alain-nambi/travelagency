'''
Created on 3 Mar 2023

@author: Famenontsoa
'''

from django import template
import traceback

register = template.Library()

# fetch fee modification history
def get_fee_history(pnr):
    from AmadeusDecoder.models.history.History import History
    history_list = []
    for history in History.objects.filter(pnr_number=pnr.number).order_by('-modification_date').all():
        temp_modification = {}
        temp_modification['modified_object'] = history.modification_type
        temp_modification['username'] = history.username
        temp_modification['modification_date'] = history.modification_date
        modif_type = {"initial_cost": "Montant initial", "new_cost": "Montant actuel", 
                      "initial_total": "Total initial", "new_total": "Total actuel", 
                      "target_object": "Billet parent"}
        history_modification = history.modification
        modification_display = "<ul>"
        for modif_type_key in modif_type:
            modification_display += "<li>" + modif_type[modif_type_key] + ': ' + history_modification[modif_type_key] + "</li>"
        modification_display += "</ul>"
        temp_modification['modification'] = modification_display
        history_list.append(temp_modification)
        
    return history_list

@register.filter(name='pnr_history')
def get_history(pnr):
    try:
        history_list = get_fee_history(pnr)
        if len(history_list) > 0:
            return history_list
    except:
        traceback.print_exc()
    return False