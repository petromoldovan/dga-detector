import json
from flask import Flask
from flask import request
import pickle
from models.train import TRAINED_MODEL_FILE
from models.feature_extraction import extract_features
import tldextract

# cache object of known/checked domains
DOMAIN_CACHE = {}
# placeholder to hold model in memory
ML_PREDICTION_MODEL = None

app = Flask(__name__)

# open file with trained model
with open(TRAINED_MODEL_FILE, 'rb') as f:
    ML_PREDICTION_MODEL = pickle.load(f)


@app.route('/', methods=['GET'])
def home():
    return json.dumps({
        'content': 'this is home screen'
    })

@app.route('/detect', methods=['POST'])
def detect():
    if not ML_PREDICTION_MODEL:
        return json.dumps({
            'error': 'ML is not calculated'
        })

    data = request.get_json()
    domain_to_examine = data.get('domain')

    sld = tldextract.extract(domain_to_examine)[1]

    # try to resolve from cache
    if sld in DOMAIN_CACHE:
        return json.dumps({
            "dga_probability": DOMAIN_CACHE[sld]
        })

    # process
    data_arr = extract_features([sld])

    # classify
    res = ML_PREDICTION_MODEL.predict_proba(data_arr)

    if not domain_to_examine:
        return json.dumps({
            'error': 'domain is not provided'
        })

    dga_probability = round(res[0][1], 3)

    # add to cache
    DOMAIN_CACHE[sld] = dga_probability

    return json.dumps({
        "dga_probability": dga_probability
    })


if __name__ == "__main__":
    app.run()
