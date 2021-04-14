import base64

from flask import Flask, request, jsonify, make_response, send_file
import json
from utils.config import DEPLOY, S3_BUCKET, PORT
from utils import Generate, upload_file_to_s3

app = Flask(__name__)


@app.route('/generate', methods=['GET'])
def generate():
    generator = Generate()
    pics = request.args.get('pics')
    if pics:
        pics = int(pics)
    else:
        pics = 1
    args = {
        'size': 512,
        'sample': 1,
        'pics': pics,
        'truncation': 1,
        'truncation_mean': 4096,
        'ckpt': 'model/prod.pt',
        'channel_multiplier': 2,
        'latent': 512,
        'n_mlp': 2
    }
    img = generator.generate(args)
    response = {}
    if DEPLOY:
        for i in range(pics):
            with open(img[i], "rb") as f:
                response[f'image{i}'] = upload_file_to_s3(f, S3_BUCKET, img[i], "image/jpeg")
    else:
        pass
    return make_response(jsonify(response), 200)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=PORT)
