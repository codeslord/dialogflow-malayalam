# -*- coding:utf8 -*-

import json

from flask import Flask, request, make_response, jsonify

import pandas as pd

import pickle

app = Flask(__name__)
log = app.logger


@app.route('/', methods=['POST'])
def webhook():
    """This method handles the http requests for the Dialogflow webhook
    This is meant to be used in conjunction with the weather Dialogflow agent
    """
    req = request.get_json(silent=True, force=True)
    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return 'json error'

    if action == 'meaning':
        res = meaning(req)

    else:
        log.error('Unexpected action.')

    print('Action: ' + action)
    print('Response: ' + res)

    return make_response(jsonify({'fulfillmentText': res}))


def meaning(req):
    with open('md.pickle', 'rb') as handle:
        md = pickle.load(handle)
    word1 = req['queryResult']['parameters']['word1']
    word2 = req['queryResult']['parameters']['word2']
    word3 = req['queryResult']['parameters']['word3']
    if any([word1, word2, word3]):
        word = word1 or word2 or word3
        return str(', '.join(map(str, md[word])))

port = int(os.getenv('PORT', 5000))
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
