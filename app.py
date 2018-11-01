import random
import requests
from flask import Flask, request
import conversation_exchange

app = Flask(__name__)
ACCESS_TOKEN = 'EAAEZASS6vBYUBANvTyvSDx2Kh5abL4XlaABj2daYwhZCK6d58FjKWPuqeSBbJChyX6qPiG6gHMgQhqsruI73jKigNtYmUFsZBEVjnxgvOzQZADpL3q6YKQIcZBsgqfC7S22ScMR1xaOMWq268utNoxkPDyhAdadNpBkqO90qfZBgZDZD'
VERIFY_TOKEN = 'ASKAMY_TOKEN'

#bot = Bot(ACCESS_TOKEN)

payloads = []

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/webhook", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       print(output)
       print ('-------------Above is the message from FB--------------')
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            sender_id = message['sender']['id']
            if message.get('message'):
                user_response = message['message'].get('text')
            elif message.get('postback'):
                user_response = message['postback'].get('title')
            #user_response = message['message'].get('text')
            print("This is the user response {}".format(user_response))
            exchange_obj = conversation_exchange.Exchange(sender_id,'FB',user_response)
            payloads = exchange_obj.start_conversation()
    
    for payload in payloads:
        
        send_message(payload)
    return "Message Processed"

 
def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def send_message(payload):
    #sends user the text message provided via input response parameter
    #bot.send_text_message(recipient_id, response)
    auth = {
    'access_token':ACCESS_TOKEN
    }
    print('Payload sent to facebook is {}\n\n'.format(payload))
    request_endpoint = 'https://graph.facebook.com/v3.2/me/messages'
    response = requests.post(
        request_endpoint,
        params=auth,
        json=payload
        )
    result = response.json()
    print("This the response sent {} \n and the result from fb{}".format('OK', result))
    return result

def get_user_details(sender_id):
    request_endpoint = 'https://graph.facebook.com/v3.2/{}?fields=first_name,last_name&access_token={}'.format(sender_id,ACCESS_TOKEN)
    response = requests.get(request_endpoint)
    user_profile_json = response.json()
    return user_profile_json

def modify_fb_messanger_profile(profile_payload):
    request_endpoint = 'https://graph.facebook.com/v3.2/me/messenger_profile?&access_token={}'.format(sender_id,ACCESS_TOKEN)
    response = requests.post(
        request_endpoint,
        json=payload
        )
    result = response.json()
    return result

if __name__ == "__main__":
    app.run()
   
