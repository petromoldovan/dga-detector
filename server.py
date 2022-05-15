import json
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return json.dumps({
        'content': 'this is home screen'
    })

@app.route('/detect', methods=['POST'])
def detect():
    data = request.get_json()
    domain_to_examine = data.get('domain')

    print("got data", data)

    if not domain_to_examine:
        return json.dumps({
            'error': 'domain is not provided'
        })

    return json.dumps(data)


# if __name__ == "__main__":
#     app.run(ssl_context='adhoc')
