import random
import requests
from flask import Flask, request
from pymessenger.bot import Bot
import conversation_exchange

app = Flask(__name__)
ACCESS_TOKEN = 'EAAGsOx87ORMBAETxCpKZB5QGy7KJZAZBN9F5lQMZBqQ8nVJKNAV7jyX5gMTNF76fJ7d9ZB1FT38CZCu3CqEwdtBhlOdP3yvR1kYcQpzZCDOSZCMZC3Ms8SWs3jTi35mWvkmrdNl24R971IaZAE0sZBf9CO6n1MzWa8cOSkigzVxbR7BnkHKovvV2IZBq'
VERIFY_TOKEN = 'tokentroy'

bot = Bot(ACCESS_TOKEN)

payloads = []

@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
       output = request.get_json()
       print(output)
       print ('-------------Above is the message from FB--------------')
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            sender_id = message['sender']['id']
            msg = message.get("message")
            if not msg: continue
            if msg.get('text'): user_response = msg.get('text')
            if msg.get('attachments'):
                attachments = msg.get('attachments')
                print(attachments)
                for attachment in attachments:
                    if attachment.get('type') == 'image':
                        print("Found Image!")
                        user_response = attachment['payload'].get('url')
                        print(user_response)
            if message.get('postback'):
                user_response = message['postback'].get('title').encode('utf-8', '')
            #user_response = message['message'].get('text')
            print("This is the user response {}".format(user_response))
            exchange_obj = conversation_exchange.Exchange(sender_id,'FB',user_response)
            payloads = exchange_obj.start_conversation()
    for payload in payloads:
        send_message(payload)
    return "Message Processed"

 
def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def send_message(payload):
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
   
