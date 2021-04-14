import base64

from flask import Flask, request, jsonify, make_response, send_file
import json

from utils import Generate

app = Flask(__name__)


@app.route('/generate', methods=['GET'])
def generate():
    generator = Generate()
    args = {
        'size': 512,
        'sample': 1,
        'pics': 3,
        'truncation': 1,
        'truncation_mean': 4096,
        'ckpt': 'model/prod.pt',
        'channel_multiplier': 2,
        'latent': 512,
        'n_mlp': 8
    }
    img = generator.generate(args)

    response = {'image0': "success"}
    return make_response(jsonify(response), 200)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
