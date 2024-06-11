from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import datetime

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:8080"}})
CORS(app, resources={r"/*": {"origins": "*"}})

client = MongoClient('mongodb://db:27017/')
db = client['mydatabase']

@app.route('/')
def home():
    return "Flask is running!"

@app.route('/upload', methods=['POST'])
def upload_data():
    try:
        data_list = request.json  # Assuming the incoming data is a list of records
        if not isinstance(data_list, list):
            return jsonify({'error': 'Invalid data format, expected a list of records'}), 400

        for data in data_list:
            if not isinstance(data, dict):
                return jsonify({'error': 'Invalid record format, expected a dictionary'}), 400

            record_id = data.get('RecordID')
            user_name = data.get('UserName')
            user_email = data.get('UserEmail')

            if not record_id or not user_name or not user_email:
                return jsonify({'error': 'RecordID, UserName, and UserEmail are required fields'}), 400

            data['upload_date'] = datetime.datetime.now(datetime.timezone.utc)

            # Check if the record with the same RecordID already exists
            existing_record = db.uploads.find_one({'RecordID': record_id})

            if existing_record:
                # Update the existing record
                db.uploads.update_one({'RecordID': record_id}, {'$set': data})
            else:
                # Insert a new record
                db.uploads.insert_one(data)

        return jsonify({'message': 'Data processed successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/uploads', methods=['GET'])
def get_uploads():
    try:
        user_email = request.args.get('UserEmail')
        query = {}
        if user_email:
            query['UserEmail'] = user_email
        # Excluding the _id field from the result
        uploads = list(db.uploads.find(query, {'_id': 0}))
        return jsonify(uploads), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
