'''
Created on 27 Aug 2022

@author: Famenontsoa
'''
from django.db import models
from AmadeusDecoder.models.BaseModel import BaseModel

class PnrAirSegments(models.Model, BaseModel):
    '''
    classdocs
    '''

    class Meta:
        db_table = 't_pnrairsegments'
    
    pnr = models.ForeignKey(
        "AmadeusDecoder.Pnr",
        on_delete=models.CASCADE,
        related_name='segments'
    )
    servicecarrier = models.ForeignKey(
        "AmadeusDecoder.Airline",
        on_delete=models.CASCADE,
        related_name='airline'
    )
    flightno = models.CharField(max_length=50, null=True)
    flightclass = models.CharField(max_length=50, null=True)
    bkgclass = models.CharField(max_length=50, null=True)
    departuretime = models.DateTimeField(null=True)
    arrivaltime = models.DateTimeField(null=True)
    codeorg = models.ForeignKey(
        "AmadeusDecoder.Airport",
        on_delete=models.CASCADE,
        to_field='iata_code',
        related_name='origin_airport',
        null=True
    )
    amanameorg = models.CharField(max_length=200, null=True)
    countryorg = models.CharField(max_length=200, null=True)
    codedest = models.ForeignKey(
        "AmadeusDecoder.Airport",
        on_delete=models.CASCADE,
        to_field='iata_code',
        related_name='destination_airport',
        null=True
    )
    amanamedest = models.CharField(max_length=200, null=True)
    countrydest = models.CharField(max_length=200, null=True)
    baggageallow = models.CharField(max_length=200, null=True)
    terminalcheckin = models.CharField(max_length=200, null=True)
    timecheckin = models.TimeField(null=True)
    segment_type = models.CharField(max_length=100, default='Flight') # flight or SVC
    other_segment_description = models.CharField(max_length=200, default='Auxiliary segment') # other description related to a segment, mainly used with SVCs
    segment_state = models.IntegerField(default=0) # 0 normal, 1 flown
    segment_hk_sa = models.CharField(max_length=10, null=True) # HK, SA, ....
    segmentorder = models.CharField(max_length=200, null=True)
    is_open = models.BooleanField(default=0) # 0 normal flight, 1 open flight
    air_segment_status = models.IntegerField(default=1) # 0 voided, 1 open
    
    # get air segment by air segment
    def get_air_segment_by_air_segment(self, pnr):
        segment = PnrAirSegments.objects.filter(pnr__id=pnr.id, flightno=self.flightno, segmentorder=self.segmentorder, codedest=self.codedest, codeorg=self.codeorg).first()
        # segment = PnrAirSegments.objects.filter(pnr__id=pnr.id, segmentorder=self.segmentorder).first()
        return segment
    
    # update air segments status on new segments
    # to be placed before segments insertion
    def update_segment_status(self, pnr, new_segments):
        if len(new_segments) > 0:
            old_segments = pnr.segments.all()
            old_segments_data = []
            for segment in old_segments:
                temp_data = {}
                temp_data['segment_obj'] = segment
                temp_data['data'] = (segment.flightno if segment.flightno is not None else '') + \
                                          (segment.segmentorder if segment.segmentorder is not None else '') + \
                                          (str(segment.departuretime) if segment.departuretime is not None else '') + \
                                          (str(segment.arrivaltime) if segment.arrivaltime is not None else '') + \
                                          (segment.flightclass if segment.flightclass is not None else '')
                old_segments_data.append(temp_data)
            
            new_segments_data = []
            for new_segment in new_segments:
                new_segments_data.append((new_segment.flightno if new_segment.flightno is not None else '') + \
                                          (new_segment.segmentorder if new_segment.segmentorder is not None else '') + \
                                          (str(new_segment.departuretime) if new_segment.departuretime is not None else '') + \
                                          (str(new_segment.arrivaltime) if new_segment.arrivaltime is not None else '') + \
                                          (new_segment.flightclass if new_segment.flightclass is not None else ''))
                
            for old_data in old_segments_data:
                if old_data['data'] not in new_segments_data:
                    old_data['segment_obj'].air_segment_status = 0
                    old_data['segment_obj'].save()
                    
                    related_ticket_segments = old_data['segment_obj'].tickets.all()
                    for related_ticket in related_ticket_segments:
                        temp_ticket = related_ticket.ticket
                        temp_ticket.state = 0
                        temp_ticket.ticket_status = 3
                        temp_ticket.save()
                        
                        # udpate pnr state
                        temp_ticket.update_pnr_state(pnr)
            
            print('OLD_DATA: ', old_segments_data)
            print('NEW_DATA: ', new_segments_data)
        
    def __str__(self):
        if self.segment_type != 'Flight':
            return 'SVC'
        else:
            return self.servicecarrier.iata + ' ' + (self.flightno if self.flightno is not None else 'OPEN')
