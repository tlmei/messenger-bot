import random
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'EAAIeg8hXB0YBAHCr9kvnZAcJQZAL8XyLskZBZBCL7RSZBVbnYp2NTmrsdIXwVRAokexg9kZAwdwcKeQf0x3BqkMg0IBBda43z5ZChWnxevq0mq3lnSmS3KZBZCMQmewkXMpcHv4DKA5nbKU3tbJIZB36xiZB3C9owwQvH7ZAv02CZATJXl4xL3VpLIJqQ'
VERIFY_TOKEN = 'tokentroy'
bot = Bot(ACCESS_TOKEN)

@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
       output = request.get_json()
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
