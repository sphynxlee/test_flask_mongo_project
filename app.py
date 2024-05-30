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
    try:
        data = request.json
        user_name = data.get('UserName')
        user_email = data.get('UserEmail')

        data['upload_date'] = datetime.datetime.now(datetime.timezone.utc)

        if user_name and user_email:
            db.uploads.insert_one(data)
            return jsonify({'message': 'Data uploaded successfully'}), 201
        else:
            return jsonify({'error': 'User ID is required'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/uploads', methods=['GET'])
def get_uploads():
    try:
        uploads = list(db.uploads.find({}, {'_id': 0}))  # Excluding the _id field from the result
        return jsonify(uploads), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
