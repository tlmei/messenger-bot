#import core_engine
import response_payload
import traceback

import copy
#from firebase_admin import firestore
from datetime import datetime, timezone
from string import Template


class Exchange(object):

    def __init__(self, member_identifier, source_platform,user_response):
        self.user_id_on_platform = member_identifier
        self.source_platform = source_platform
        #self.core_engine_obj=core_engine_obj
        self.user_response = user_response

    def start_conversation(self):
        payloads = []
        #core_engine_obj.update_member_details(core_engine_obj.get_member(),user_details)
        payload = {}
        #conversation_ref = core_engine_obj.add_conversation(core_engine_obj.get_member())
        #first_name = self.core_engine_obj.get_member().get().to_dict().get('first_name')
        #print('First Name from DB is {}'.format(first_name))

        conversation_id = 'None'
        if self.user_response != None:
            payload = response_payload.fb_payload('receiving_img', '...', self.user_id_on_platform, conversation_id, payload, self.user_response)

        #payload = response_payload.fb_payload('welcome_user','...',self.user_id_on_platform,conversation_id,payload)
        #payload['message']['attachment']['payload']['text'] = Template(payload['message']['attachment']['payload'].get('text')).safe_substitute(arg1=first_name)
        
        #del payload['platform']
        payloads.append(payload)
        print('This is the payload in exchange about to be send to fb {}'.format(payloads))
        return payloads
