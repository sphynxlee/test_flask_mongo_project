
# test_flask_project Setup Guide

## 1. Install Docker

Make sure you have Docker installed on your local machine. If not, please refer to the following links:
- [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
- [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
- [Docker for Linux](https://docs.docker.com/engine/install/)

## 2. Create Project Directory and Files

Create a new project directory in your working directory and navigate to it:
```bash
mkdir test_flask_project
cd test_flask_project
```

## 3. Create Flask Application

Create an `app.py` file in the project directory:
```python
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
    data['upload_date'] = datetime.datetime.utcnow()

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
```

## 4. Create Dependencies File

Create a `requirements.txt` file in the project directory, listing Flask and pymongo dependencies:
```plaintext
Flask==3.0.3
pymongo==4.7.2
```

## 5. Create Dockerfile

Create a `Dockerfile` in the project directory, defining how to build your Docker image:
```Dockerfile
# Use official Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install project dependencies
RUN pip install -r requirements.txt

# Expose application port
EXPOSE 5000

# Run Flask application
CMD ["python", "app.py"]
```

## 6. Create Docker Compose File

Create a `docker-compose.yml` file in the project directory, defining multi-container application services:
```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "5001:5000"
    volumes:
      - .:/app
    environment:
      - FLASK_ENV=development
  db:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db

volumes:
  mongo-data:
```

## 7. Start Docker Containers

Start Docker containers in the project directory:
```bash
docker-compose up --build
```

## 8. Test Flask Application

Access `http://localhost:5001` in your browser, you should see "Flask is running!".

Test POST request using `curl` or Postman:
```bash
curl -X POST http://localhost:5001/upload -H "Content-Type: application/json" -d '{"user_id": "12345", "data": "sample data"}'
```

Test GET request using `curl` or Postman:
```bash
curl http://localhost:5001/uploads
```

## 9. View Data in MongoDB

Use MongoDB client tools (such as  MongoDB Compass) to connect to `localhost:27017` and view the data in the `uploads` collection of the `mydatabase` database.

## 10. Stop and Restart Docker Containers

Stop Docker containers:
```bash
docker-compose down
```

Restart Docker containers:
```bash
docker-compose up --build
```

## Other Commands and Tips

- **View Docker Container Logs**:
  ```bash
  docker-compose logs web
  ```

- **Enter MongoDB Container**:
  ```bash
  docker-compose exec db bash
  ```

- **Install `mongo` Command Line Tools in MongoDB Container**:
  ```bash
  apt-get update
  apt-get install -y mongo-tools
  ```
