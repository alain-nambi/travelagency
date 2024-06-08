import ast
import json
from AmadeusDecoder.models.pnr.Passenger import Passenger
from AmadeusDecoder.models.pnr.Pnr import UnremountedPnr
from AmadeusDecoder.models.pnrelements.PnrAirSegments import PnrAirSegments
from AmadeusDecoder.models.utilities.Comments import Anomalie, Comment
from datetime import date, timedelta
from django import template
from django.db.models.fields import BooleanField
from django.db.models import Value, Q
from django.http import JsonResponse
from AmadeusDecoder.models.invoice.Ticket import Ticket

register = template.Library()

@register.filter(name="add_hours_plus_three")
def set_add_hours_plus_three(date):
    return date + timedelta(hours=3)

@register.filter(name='response')
def get_response(pnr_id):
    from AmadeusDecoder.models.utilities.Comments import Response
    try:
        response = Response.objects.filter(pnr_id__id=pnr_id).last()
        if response is not None:
            return response.response
        else:
            return ''
    except:
        return ''
    
@register.filter(name="comment_state")
def get_comment_state(comment_id):
    maximum_timezone = "2023-01-01 01:00:00.000000+03:00"
    

    count_comment_state_true = Comment.objects.filter(Q(creation_date__gt=maximum_timezone)).filter(state=True).count()
    count_comment_state_false = Comment.objects.filter(Q(creation_date__gt=maximum_timezone) ).filter(state=False).count()
    
    context = {}
    context["false"] = count_comment_state_false
    context["true"] = count_comment_state_true
        
    return context

# return anomaly comments
@register.filter(name='anomaly_comments')
def get_anomaly_comment_by_pnr(pnr):
    from AmadeusDecoder.models.utilities.Comments import Comment
    from AmadeusDecoder.models.utilities.Comments import Response
    comments = Comment.objects.filter(pnr_id_id=pnr.id).all()
    responses = Response.objects.filter(pnr_id_id=pnr.id).all()    
    comments_qs = comments.values(
                    'comment', 
                    'pnr_id_id', 
                    'user_id_id', 
                    'creation_date'
                ).annotate(
                    sender=Value(True, output_field=BooleanField())
                )
    responses_qs = responses.values(
                    'response', 
                    'pnr_id_id', 
                    'user_id_id', 
                    'creation_date'
                ).annotate(
                    receiver=Value(False, output_field=BooleanField())
                )
    result = comments_qs.union(responses_qs)
    if len(result) > 0:
        return result.order_by("creation_date")
    else:
        return None

# return a username of user object
@register.filter(name='username')
def get_username_by_user(user_id):
    from AmadeusDecoder.models.user.Users import User
    user = User.objects.get(id=user_id)
    return user.username

# return a text stripped of whitespace
@register.filter(name='strip')
def strip(word):
    return word.strip()

@register.simple_tag(name='anomaly_state')
def get_anomaly_state():
    count_anomaly_state_true = Anomalie.objects.filter(status=0).count()
    count_anomaly_state_false = Anomalie.objects.filter(status=1).count()
    
    context = {
        "false": count_anomaly_state_false,
        "true": count_anomaly_state_true,
    }
        
    return context
        
@register.filter(name='correct_datetime')
def get_correct_datetime(hours):
    correct_date = hours + timedelta(hours=3)
    return correct_date.strftime("%b. %d, %Y, %H:%M")

# to verify if there is new anomaly on the pnr
@register.filter(name='new_anomalie')
def new_anomalie(pnr):
    anomalies = Anomalie.objects.filter(pnr_id=pnr.id ,status=0).all()
    if anomalies.exists():
        return anomalies.count()
    return None

@register.filter(name='get_details')
def get_details(anomalie):
    anomalie = Anomalie.objects.get(pk=anomalie.id)
    #transformer le string "['84560','84562']" en liste
    print(anomalie.infos.get('ticket_status'))
    print(type(anomalie.infos.get('ticket_status')))
    if int(anomalie.infos.get('ticket_status')) == 1:
        segment_id = ast.literal_eval(anomalie.infos.get('segment'))

        segments_list = []
        if segment_id != "":
            if isinstance(segment_id, list):
                for element in segment_id:
                    segments = PnrAirSegments.objects.get(pk=element)
                    segments_list.append(str(segments)+' '+str(segments.segmentorder))
            elif isinstance(segment_id, int):
                segments = PnrAirSegments.objects.get(pk=segment_id)
                segments_list.append(str(segments)+' '+str(segments.segmentorder))
                
            segment= ','.join(segments_list)
        else:
            segment = ""
        
        passenger = Passenger.objects.get(pk=anomalie.infos.get('passenger_id'))

        context ={}
        context['passenger'] = passenger
        context['segment'] = segment
        return context
    else:
        print('----ELSE------------')
        return ""

# pnr non remonte count state
@register.simple_tag(name='unremounted_pnr_state')
def get_anomaly_state():
    count_anomaly_state_true = UnremountedPnr.objects.filter(state=1).count()
    count_anomaly_state_false = UnremountedPnr.objects.filter(state=0).count()
    
    context = {
        "false": count_anomaly_state_false,
        "true": count_anomaly_state_true,
    }
        
    return context