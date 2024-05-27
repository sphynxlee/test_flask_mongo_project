from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime

app = Flask(__name__)

client = MongoClient('mongodb://db:27017/')
db = client['mydatabase']

@app.route('/')
def home():
    return "Flask is running!"

@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.json
    user_id = data.get('user_id')
    data['upload_date'] = datetime.datetime.now(datetime.timezone.utc)

    if user_id:
        db.uploads.insert_one(data)
        return jsonify({'message': 'Data saved successfully'}), 201
    else:
        return jsonify({'error': 'User ID is required'}), 400

@app.route('/uploads', methods=['GET'])
def get_uploads():
    uploads = list(db.uploads.find({}, {'_id': 0}))
    return jsonify(uploads), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)