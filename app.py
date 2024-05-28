from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime
import jwt
import requests

app = Flask(__name__)

client = MongoClient('mongodb://db:27017/')
db = client['mydatabase']

APP_CLIENT_ID = "your-tenat-id"
TENANT_ID = "your-tenant-id"

def verify_token(token):
    # Microsoft public key endpoint
    jwks_uri = "https://login.microsoftonline.com/common/discovery/v2.0/keys"
    jwks = requests.get(jwks_uri).json()
    public_keys = {jwk['kid']: jwt.algorithms.RSAAlgorithm.from_jwk(jwt.json.dumps(jwk)) for jwk in jwks['keys']}
    kid = jwt.get_unverified_header(token)['kid']
    public_key = public_keys[kid]
    # decode and verify the token
    decoded = jwt.decode(token, public_key, algorithms=['RS256'], audience='{APP_CLIENT_ID}', issuer='https://login.microsoftonline.com/{TENANT_ID}/v2.0')
    return decoded

@app.route('/')
def home():
    return "Flask is running!"

@app.route('/upload', methods=['POST'])
def upload_data():
    # Assumes Bearer token
    token = request.headers.get('Authorization').split()[1]
    try:
        decoded = verify_token(token)
        data = request.json
        user_id = data.get('user_id')
        data['upload_date'] = datetime.datetime.now(datetime.timezone.utc)

        if user_id:
            db.uploads.insert_one(data)
            return jsonify({'message': 'Data uploaded successfully'}), 201
        else:
            return jsonify({'error': 'User ID is required'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/uploads', methods=['GET'])
def get_uploads():
    uploads = list(db.uploads.find({}, {'_id': 0}))
    return jsonify(uploads), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
