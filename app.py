import random
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'EAAGsOx87ORMBAETxCpKZB5QGy7KJZAZBN9F5lQMZBqQ8nVJKNAV7jyX5gMTNF76fJ7d9ZB1FT38CZCu3CqEwdtBhlOdP3yvR1kYcQpzZCDOSZCMZC3Ms8SWs3jTi35mWvkmrdNl24R971IaZAE0sZBf9CO6n1MzWa8cOSkigzVxbR7BnkHKovvV2IZBq'
VERIFY_TOKEN = 'tokentroy'
bot = Bot(ACCESS_TOKEN)

@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
       output = request.get_json()
       print(output)
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = get_message()
                    send_message(recipient_id, response_sent_text)
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"

def verify_fb_token(token_sent):
	if token_sent == VERIFY_TOKEN:
		return request.args.get("hub.challenge")
	return 'Invalid verification token'

def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == '__main__':
	app.run()
