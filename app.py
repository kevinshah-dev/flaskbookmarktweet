from flask import Flask, redirect, url_for, session, request, jsonify
import tweepy
import os

consumer_token = "8nKoJIb7IC7mQRyJCqC5lPbj9"
consumer_secret = "7MMpibQpFbE11EklSPOCFdUtjsVEQClvil2JPC9RFaFwlvryJq"
callback_url = "http://localhost:3000/twitter_callback"


#auth = tweepy.OAuthHandler(consumer_token, consumer_secret, callback_url)

app = Flask(__name__)


@app.route('/')
def index():
    print("Hello World")
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Use 8080 as default
    app.run(debug=True, host='0.0.0.0', port=port)
