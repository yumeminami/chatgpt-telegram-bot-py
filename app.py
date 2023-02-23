# from user.user import User
# import tiktoken
# from utils.redis import GetRedis, SetRedis,InitRedis
# test_map = {}
import redis

# def update(id, **kwargs):
#     if id not in test_map:
#         test_map[id] = User(id)
#     for key, value in kwargs.items():
#         setattr(test_map[id], key, value)


# def main():
#     # update(1)
#     # # print test_map[1] all attributes
#     # print(test_map[1].user_id)
#     # print(test_map[1].previous_message)
#     # print(test_map[1].mode)

#     # update(1, previous_message="test")
#     # print(test_map[1].user_id)
#     # print(test_map[1].previous_message)
#     # print(test_map[1].mode)

#     # update(1, mode="images")
#     # print(test_map[1].user_id)
#     # print(test_map[1].previous_message)
#     # print(test_map[1].mode)
#     # enc = tiktoken.encoding_for_model("text-davinci-003")
#     # print(len(enc.encode_ordinary("")))

#     InitRedis()
#     SetRedis("test","test")
#     print(GetRedis("test"))

# def main():
#     redis_client = redis.Redis(host="localhost", port=6379, db=0, password="frM991103")
#     redis_client.set("test", "test")
#     print(redis_client.get("test"))


# if __name__ == "__main__":
#     main()

# app.py
#
# Use this sample code to handle webhook events in your integration.
#
# 1) Paste this code into a new file (app.py)
#
# 2) Install dependencies
#   pip3 install flask
#   pip3 install stripe
#
# 3) Run the server on http://localhost:4242
#   python3 -m flask run --port=4242

# import json
# import os
# import stripe

# # from flask import Flask, jsonify, request
# # This is your Stripe CLI webhook secret for testing your endpoint locally.
# endpoint_secret = 'whsec_bca9465a70ce33fd92ed8c023beee6021e1f923c0e48e620ee8f4dfeba580c14'

# # app = Flask(__name__)

# from fastapi import FastAPI
# from fastapi import Request
# app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# @app.post("/webhook")
# async def webhook(request: Request):
#     event = None
#     payload = request.data
#     sig_header = request.headers['STRIPE_SIGNATURE']

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
#     except ValueError as e:
#         # Invalid payload
#         raise e
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         raise e

#     # Handle the event
#     if event['type'] == 'checkout.session.async_payment_failed':
#       session = event['data']['object']
#     elif event['type'] == 'checkout.session.async_payment_succeeded':
#       session = event['data']['object']
#     elif event['type'] == 'checkout.session.completed':
#       session = event['data']['object']
#     elif event['type'] == 'checkout.session.expired':
#       session = event['data']['object']
#     # ... handle other event types
#     else:
#       print('Unhandled event type {}'.format(event['type']))


# app.py
#
# Use this sample code to handle webhook events in your integration.
#
# 1) Paste this code into a new file (app.py)
#
# 2) Install dependencies
#   pip3 install flask
#   pip3 install stripe
#
# 3) Run the server on http://localhost:4242
#   python3 -m flask run --port=4242

# import json
# import os
# import stripe

# from flask import Flask, jsonify, request

# # This is your Stripe CLI webhook secret for testing your endpoint locally.
# endpoint_secret = 'whsec_bca9465a70ce33fd92ed8c023beee6021e1f923c0e48e620ee8f4dfeba580c14'

# app = Flask(__name__)

# @app.route('/', methods=['GET'])
# def index():
#     return 'Hello World'

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     event = None
#     payload = request.data
#     sig_header = request.headers['STRIPE_SIGNATURE']

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
#     except ValueError as e:
#         # Invalid payload
#         raise e
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         raise e

#     # Handle the event
#     if event['type'] == 'payment_intent.succeeded':
#       payment_intent = event['data']['object']
#     # ... handle other event types
#     else:
#       print('Unhandled event type {}'.format(event['type']))

#     return jsonify(success=True)


# app.py
#
# Use this sample code to handle webhook events in your integration.
#
# 1) Paste this code into a new file (app.py)
#
# 2) Install dependencies
#   pip3 install flask
#   pip3 install stripe
#
# 3) Run the server on http://localhost:4242
#   python3 -m flask run --port=4242

import json
import os
import stripe

from flask import Flask, jsonify, request

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = 'whsec_LkoRwwk4LbtREFay3GyMDhK7oUUJa0KD'

app = Flask(__name__)
@app.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'checkout.session.async_payment_failed':
        session = event['data']['object']
        print('Payment failed')
    elif event['type'] == 'checkout.session.async_payment_succeeded':
        session = event['data']['object']
        print('Payment succeeded')
    elif event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print('Payment completed')
    elif event['type'] == 'checkout.session.expired':
        session = event['data']['object']
        print('Payment expired')
    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)
