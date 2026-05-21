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

    all_quizzes = {
        'taj_mahal': [
            {'question': 'In which city is the Taj Mahal located?', 'options': ['Delhi', 'Agra', 'Jaipur', 'Lucknow'], 'answer': 'Agra'},
            {'question': 'Who built the Taj Mahal?', 'options': ['Akbar', 'Humayun', 'Shah Jahan', 'Aurangzeb'], 'answer': 'Shah Jahan'},
            {'question': 'How many years did it take to build the Taj Mahal?', 'options': ['10 years', '15 years', '22 years', '30 years'], 'answer': '22 years'},
            {'question': 'The Taj Mahal was built in memory of whom?', 'options': ['Nur Jahan', 'Mumtaz Mahal', 'Razia Sultana', 'Jodha Bai'], 'answer': 'Mumtaz Mahal'},
            {'question': 'What is the Taj Mahal made of?', 'options': ['Red sandstone', 'White marble', 'Granite', 'Limestone'], 'answer': 'White marble'}
        ],
        'red_fort': [
            {'question': 'Who built the Red Fort?', 'options': ['Akbar', 'Humayun', 'Shah Jahan', 'Aurangzeb'], 'answer': 'Shah Jahan'},
            {'question': 'In which city is the Red Fort located?', 'options': ['Agra', 'Jaipur', 'Delhi', 'Lucknow'], 'answer': 'Delhi'},
            {'question': 'What is the Red Fort made of?', 'options': ['White marble', 'Red sandstone', 'Granite', 'Brick'], 'answer': 'Red sandstone'},
            {'question': 'When was the Red Fort built?', 'options': ['1539', '1639', '1739', '1839'], 'answer': '1639'},
            {'question': 'What happens at Red Fort every Independence Day?', 'options': ['Republic Day parade', 'PM hoists national flag', 'Cricket match', 'Music festival'], 'answer': 'PM hoists national flag'}
        ],
        'qutub_minar': [
            {'question': 'How tall is Qutub Minar?', 'options': ['52 metres', '62 metres', '72 metres', '82 metres'], 'answer': '72 metres'},
            {'question': 'Who built Qutub Minar?', 'options': ['Shah Jahan', 'Akbar', 'Qutub-ud-din Aibak', 'Humayun'], 'answer': 'Qutub-ud-din Aibak'},
            {'question': 'How many steps are inside Qutub Minar?', 'options': ['279', '379', '479', '579'], 'answer': '379'},
            {'question': 'In which city is Qutub Minar located?', 'options': ['Agra', 'Jaipur', 'Delhi', 'Mumbai'], 'answer': 'Delhi'},
            {'question': 'When was Qutub Minar built?', 'options': ['1093', '1193', '1293', '1393'], 'answer': '1193'}
        ],
        'india_gate': [
            {'question': 'How tall is India Gate?', 'options': ['32 metres', '42 metres', '52 metres', '62 metres'], 'answer': '42 metres'},
            {'question': 'Who designed India Gate?', 'options': ['Sir Edwin Lutyens', 'Herbert Baker', 'Le Corbusier', 'Charles Correa'], 'answer': 'Sir Edwin Lutyens'},
            {'question': 'When was India Gate built?', 'options': ['1911', '1921', '1931', '1941'], 'answer': '1931'},
            {'question': 'India Gate was built to honor soldiers of which war?', 'options': ['World War II', 'World War I', 'Indo-Pak War', 'Kargil War'], 'answer': 'World War I'},
            {'question': 'What is the name of the eternal flame at India Gate?', 'options': ['Amar Jyoti', 'Amar Jawan Jyoti', 'Shaheed Jyoti', 'Veer Jyoti'], 'answer': 'Amar Jawan Jyoti'}
        ],
        'charminar': [
            {'question': 'What does Charminar mean?', 'options': ['Three minarets', 'Four minarets', 'Five minarets', 'Six minarets'], 'answer': 'Four minarets'},
            {'question': 'In which city is Charminar located?', 'options': ['Chennai', 'Bangalore', 'Hyderabad', 'Mumbai'], 'answer': 'Hyderabad'},
            {'question': 'When was Charminar built?', 'options': ['1491', '1541', '1591', '1641'], 'answer': '1591'},
            {'question': 'How tall is each minaret of Charminar?', 'options': ['36 metres', '46 metres', '56 metres', '66 metres'], 'answer': '56 metres'},
            {'question': 'Why was Charminar built?', 'options': ['To mark a military victory', 'To celebrate end of plague', 'As a royal palace', 'As a watchtower'], 'answer': 'To celebrate end of plague'}
        ]
    }

    # Match predicted landmark to quiz
    questions = all_quizzes.get(landmark_name, all_quizzes['taj_mahal'])

    return jsonify({
        'landmark': landmark_name,
        'questions': questions
    })
    return jsonify(quiz)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)