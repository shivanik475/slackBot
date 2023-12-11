import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.web import SlackResponse

# Initialize Slack client with your OAuth token
client = WebClient(token=os.environ['xoxp-6307632625222-6323538869890-6323517896483-d5338cdc395ede9908a4c8c5ccbc4a19'])

# Function to send a message to a channel
def send_message(channel: str, message: str) -> SlackResponse:
    try:
        response = client.chat_postMessage(channel=channel, text=message)
        return response
    except SlackApiError as e:
        return f"Error sending message: {e.response['error']}"

# Bot logic
def handle_message(event_data: dict):
    text = event_data['event']['text']
    channel = event_data['event']['channel']
    if 'hello' in text.lower():
        user = event_data['event']['user']
        send_message(channel, f"Hello <@{user}>!")

# Flask application to handle events
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/events', methods=['POST'])
def events():
    data = request.json
    if 'event' in data:
        handle_message(data)
    return jsonify({"success": True})

# Start your app
if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 3000)))
