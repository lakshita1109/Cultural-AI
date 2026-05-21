from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys

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
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    result = predict_landmark(filepath)
    return jsonify(result)

@app.route('/quiz/<landmark_name>', methods=['GET'])
def get_quiz(landmark_name):
    all_quizzes = {
        'taj_mahal': [
            {'question': 'In which city is the Taj Mahal located?', 'options': ['Delhi', 'Agra', 'Jaipur', 'Lucknow'], 'answer': 'Agra'},
            {'question': 'Who built the Taj Mahal?', 'options': ['Akbar', 'Humayun', 'Shah Jahan', 'Aurangzeb'], 'answer': 'Shah Jahan'},
            {'question': 'How many years did it take to build?', 'options': ['10 years', '15 years', '22 years', '30 years'], 'answer': '22 years'},
            {'question': 'Built in memory of whom?', 'options': ['Nur Jahan', 'Mumtaz Mahal', 'Razia Sultana', 'Jodha Bai'], 'answer': 'Mumtaz Mahal'},
            {'question': 'What is the Taj Mahal made of?', 'options': ['Red sandstone', 'White marble', 'Granite', 'Limestone'], 'answer': 'White marble'}
        ],
        'red_fort': [
            {'question': 'Who built the Red Fort?', 'options': ['Akbar', 'Humayun', 'Shah Jahan', 'Aurangzeb'], 'answer': 'Shah Jahan'},
            {'question': 'Where is the Red Fort located?', 'options': ['Agra', 'Jaipur', 'Delhi', 'Lucknow'], 'answer': 'Delhi'},
            {'question': 'What is the Red Fort made of?', 'options': ['White marble', 'Red sandstone', 'Granite', 'Brick'], 'answer': 'Red sandstone'},
            {'question': 'When was the Red Fort built?', 'options': ['1539', '1639', '1739', '1839'], 'answer': '1639'},
            {'question': 'What happens at Red Fort on Independence Day?', 'options': ['Republic Day parade', 'PM hoists national flag', 'Cricket match', 'Music festival'], 'answer': 'PM hoists national flag'}
        ],
        'qutub_minar': [
            {'question': 'How tall is Qutub Minar?', 'options': ['52 metres', '62 metres', '72 metres', '82 metres'], 'answer': '72 metres'},
            {'question': 'Who built Qutub Minar?', 'options': ['Shah Jahan', 'Akbar', 'Qutub-ud-din Aibak', 'Humayun'], 'answer': 'Qutub-ud-din Aibak'},
            {'question': 'How many steps inside Qutub Minar?', 'options': ['279', '379', '479', '579'], 'answer': '379'},
            {'question': 'Where is Qutub Minar located?', 'options': ['Agra', 'Jaipur', 'Delhi', 'Mumbai'], 'answer': 'Delhi'},
            {'question': 'When was Qutub Minar built?', 'options': ['1093', '1193', '1293', '1393'], 'answer': '1193'}
        ],
        'india_gate': [
            {'question': 'How tall is India Gate?', 'options': ['32 metres', '42 metres', '52 metres', '62 metres'], 'answer': '42 metres'},
            {'question': 'Who designed India Gate?', 'options': ['Sir Edwin Lutyens', 'Herbert Baker', 'Le Corbusier', 'Charles Correa'], 'answer': 'Sir Edwin Lutyens'},
            {'question': 'When was India Gate built?', 'options': ['1911', '1921', '1931', '1941'], 'answer': '1931'},
            {'question': 'India Gate honors soldiers of which war?', 'options': ['World War II', 'World War I', 'Indo-Pak War', 'Kargil War'], 'answer': 'World War I'},
            {'question': 'What is the eternal flame at India Gate called?', 'options': ['Amar Jyoti', 'Amar Jawan Jyoti', 'Shaheed Jyoti', 'Veer Jyoti'], 'answer': 'Amar Jawan Jyoti'}
        ],
        'charminar': [
            {'question': 'What does Charminar mean?', 'options': ['Three minarets', 'Four minarets', 'Five minarets', 'Six minarets'], 'answer': 'Four minarets'},
            {'question': 'Where is Charminar located?', 'options': ['Chennai', 'Bangalore', 'Hyderabad', 'Mumbai'], 'answer': 'Hyderabad'},
            {'question': 'When was Charminar built?', 'options': ['1491', '1541', '1591', '1641'], 'answer': '1591'},
            {'question': 'How tall is each minaret?', 'options': ['36 metres', '46 metres', '56 metres', '66 metres'], 'answer': '56 metres'},
            {'question': 'Why was Charminar built?', 'options': ['Military victory', 'End of plague', 'Royal palace', 'Watchtower'], 'answer': 'End of plague'}
        ],
        'hampi': [
            {'question': 'Hampi was capital of which empire?', 'options': ['Mughal Empire', 'Maratha Empire', 'Vijayanagara Empire', 'Chola Empire'], 'answer': 'Vijayanagara Empire'},
            {'question': 'In which state is Hampi?', 'options': ['Tamil Nadu', 'Kerala', 'Andhra Pradesh', 'Karnataka'], 'answer': 'Karnataka'},
            {'question': 'Which river flows alongside Hampi?', 'options': ['Godavari', 'Tungabhadra', 'Krishna', 'Cauvery'], 'answer': 'Tungabhadra'},
            {'question': 'When did Hampi become UNESCO site?', 'options': ['1976', '1986', '1996', '2006'], 'answer': '1986'},
            {'question': 'How many surviving remains does Hampi have?', 'options': ['600', '900', '1200', '1600'], 'answer': '1600'}
        ],
        'lotus_temple': [
            {'question': 'What shape is the Lotus Temple?', 'options': ['Star', 'Lotus flower', 'Dome', 'Pyramid'], 'answer': 'Lotus flower'},
            {'question': 'When was Lotus Temple built?', 'options': ['1966', '1976', '1986', '1996'], 'answer': '1986'},
            {'question': 'How many petals does it have?', 'options': ['17', '22', '27', '32'], 'answer': '27'},
            {'question': 'Which religion runs Lotus Temple?', 'options': ['Hindu', 'Muslim', 'Bahai', 'Buddhist'], 'answer': 'Bahai'},
            {'question': 'How many people can it hold?', 'options': ['500', '1000', '1500', '2500'], 'answer': '2500'}
        ],
        'ajanta_caves': [
            {'question': 'How many caves in Ajanta?', 'options': ['20', '25', '30', '35'], 'answer': '30'},
            {'question': 'In which state are Ajanta Caves?', 'options': ['Gujarat', 'Maharashtra', 'Madhya Pradesh', 'Rajasthan'], 'answer': 'Maharashtra'},
            {'question': 'Which religion do Ajanta Caves represent?', 'options': ['Hinduism', 'Jainism', 'Buddhism', 'Sikhism'], 'answer': 'Buddhism'},
            {'question': 'When were Ajanta Caves rediscovered?', 'options': ['1719', '1769', '1819', '1869'], 'answer': '1819'},
            {'question': 'When did Ajanta become UNESCO site?', 'options': ['1973', '1978', '1983', '1988'], 'answer': '1983'}
        ],
        'gateway_of_india': [
            {'question': 'How tall is Gateway of India?', 'options': ['16 metres', '21 metres', '26 metres', '31 metres'], 'answer': '26 metres'},
            {'question': 'Where is Gateway of India?', 'options': ['Delhi', 'Chennai', 'Kolkata', 'Mumbai'], 'answer': 'Mumbai'},
            {'question': 'When was Gateway of India built?', 'options': ['1904', '1914', '1924', '1934'], 'answer': '1924'},
            {'question': 'It overlooks which sea?', 'options': ['Bay of Bengal', 'Arabian Sea', 'Indian Ocean', 'Laccadive Sea'], 'answer': 'Arabian Sea'},
            {'question': 'Who visited India inspiring its construction?', 'options': ['Queen Victoria', 'King George V', 'King Edward VII', 'Prince Charles'], 'answer': 'King George V'}
        ]
    }

    questions = all_quizzes.get(landmark_name, all_quizzes['taj_mahal'])
    return jsonify({
        'landmark': landmark_name,
        'questions': questions
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)