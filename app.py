import os
import sys
import json
import requests

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify():
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.challenge'):
        if not request.args.get('hub.verify_token') == os.environ['VERIFY_TOKEN']:
            return 'Verification token misatch', 403
        return request.args['hub.challenge'], 200

    return 'hello heroku', 200

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
