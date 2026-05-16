from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys

# Add parent directory to path so we can import model_predict
sys.path.append(os.path.dirname(__file__))
from model_predict import predict_landmark

app = Flask(__name__)
CORS(app)

FRONTEND_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'frontend')
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return send_from_directory(FRONTEND_FOLDER, 'index.html')

@app.route('/<path:filename>')
def serve_frontend(filename):
    return send_from_directory(FRONTEND_FOLDER, filename)

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image received'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    # Save uploaded image
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Run real AI prediction
    result = predict_landmark(filepath)

    return jsonify(result)

@app.route('/quiz/<landmark_name>', methods=['GET'])
def get_quiz(landmark_name):
    quiz = {
        'landmark': landmark_name,
        'questions': [
            {
                'question': 'In which city is the Taj Mahal located?',
                'options': ['Delhi', 'Agra', 'Jaipur', 'Lucknow'],
                'answer': 'Agra'
            },
            {
                'question': 'Who built the Taj Mahal?',
                'options': ['Akbar', 'Humayun', 'Shah Jahan', 'Aurangzeb'],
                'answer': 'Shah Jahan'
            }
        ]
    }
    return jsonify(quiz)

if __name__ == '__main__':
    app.run(debug=True, port=5000)