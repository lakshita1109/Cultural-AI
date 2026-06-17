import subprocess
import sys
import os

# ===== RUNTIME CLIP INSTALLATION =====
# This runs when your app starts on Vercel
try:
    import clip
    print("✅ CLIP already installed")
except ImportError:
    print("📦 Installing CLIP at runtime...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", 
        "--no-cache-dir", 
        "git+https://github.com/openai/CLIP.git"
    ])
    import clip
    print("✅ CLIP installed successfully")
# ======================================

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys

sys.path.append(os.path.dirname(__file__))
from clip_predict import predict_landmark

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
        ],
        "bidar_fort": [
            {"question": "Who built Bidar Fort?", "options": ["Hyder Ali", "Ahmad Shah Wali", "Tipu Sultan", "Adil Shah"], "answer": "Ahmad Shah Wali"},
            {"question": "When was Bidar Fort built?", "options": ["1332", "1382", "1432", "1482"], "answer": "1432"},
            {"question": "What is the perimeter of Bidar Fort?", "options": ["5 km", "7 km", "10 km", "15 km"], "answer": "10 km"},
            {"question": "What unique craft originated in Bidar?", "options": ["Channapatna toys", "Bidriware", "Ilkal saree", "Kasuti embroidery"], "answer": "Bidriware"},
            {"question": "How many bastions does Bidar Fort have?", "options": ["17", "27", "37", "47"], "answer": "37"}
        ],
        "virupaksha_temple": [
            {"question": "Where is Virupaksha Temple located?", "options": ["Mysore", "Hampi", "Bijapur", "Badami"], "answer": "Hampi"},
            {"question": "Which god is Virupaksha Temple dedicated to?", "options": ["Vishnu", "Brahma", "Shiva", "Ganesha"], "answer": "Shiva"},
            {"question": "How tall is the main tower of Virupaksha Temple?", "options": ["30 metres", "40 metres", "50 metres", "60 metres"], "answer": "50 metres"},
            {"question": "How many years has Virupaksha Temple been in continuous worship?", "options": ["500 years", "800 years", "1000 years", "1300 years"], "answer": "1300 years"},
            {"question": "Virupaksha Temple was the royal temple of which empire?", "options": ["Mughal Empire", "Maratha Empire", "Vijayanagara Empire", "Chola Empire"], "answer": "Vijayanagara Empire"}
        ],
        "mysore_palace": [
            {"question": "What is Mysore Palace also known as?", "options": ["Amba Vilas Palace", "Raj Vilas Palace", "Lal Mahal", "Fateh Mahal"], "answer": "Amba Vilas Palace"},
            {"question": "How many bulbs illuminate Mysore Palace?", "options": ["50,000", "75,000", "100,000", "150,000"], "answer": "100,000"},
            {"question": "Which dynasty built Mysore Palace?", "options": ["Wadiyar dynasty", "Hoysala dynasty", "Chalukya dynasty", "Nayaka dynasty"], "answer": "Wadiyar dynasty"},
            {"question": "Mysore Palace is the second most visited monument after which?", "options": ["Red Fort", "Qutub Minar", "Taj Mahal", "India Gate"], "answer": "Taj Mahal"},
            {"question": "How many Hindu temples are within Mysore Palace premises?", "options": ["5", "8", "12", "15"], "answer": "12"}
        ],
        "gol_gumbaz": [
            {"question": "What does Gol Gumbaz mean?", "options": ["Black dome", "Round dome", "Golden dome", "White dome"], "answer": "Round dome"},
            {"question": "Where is Gol Gumbaz located?", "options": ["Mysore", "Hampi", "Bijapur", "Badami"], "answer": "Bijapur"},
            {"question": "How many times does sound echo in Gol Gumbaz?", "options": ["3 times", "5 times", "7 times", "9 times"], "answer": "7 times"},
            {"question": "What is the diameter of the Gol Gumbaz dome?", "options": ["27 metres", "37 metres", "47 metres", "57 metres"], "answer": "37 metres"},
            {"question": "Gol Gumbaz has the second largest dome after which monument?", "options": ["Taj Mahal", "St. Peter's Basilica", "Pantheon", "Hagia Sophia"], "answer": "St. Peter's Basilica"}
        ],
        "badami_caves": [
            {"question": "How many main cave temples are in Badami?", "options": ["2", "3", "4", "5"], "answer": "4"},
            {"question": "Which dynasty built Badami Caves?", "options": ["Hoysala", "Chalukya", "Rashtrakuta", "Pallava"], "answer": "Chalukya"},
            {"question": "Which cave in Badami is dedicated to Jain saints?", "options": ["Cave 1", "Cave 2", "Cave 3", "Cave 4"], "answer": "Cave 4"},
            {"question": "Badami was the capital of which kingdom?", "options": ["Hoysala kingdom", "Early Chalukya kingdom", "Vijayanagara Empire", "Nayaka kingdom"], "answer": "Early Chalukya kingdom"},
            {"question": "What material are the Badami caves carved from?", "options": ["Granite", "Marble", "Sandstone", "Limestone"], "answer": "Sandstone"}
        ],
        "belur_temple": [
            {"question": "How long did it take to build Chennakeshava Temple?", "options": ["50 years", "75 years", "103 years", "150 years"], "answer": "103 years"},
            {"question": "Who built the Chennakeshava Temple at Belur?", "options": ["Vikramaditya", "Vishnuvardhana", "Ballala", "Narasimha"], "answer": "Vishnuvardhana"},
            {"question": "What was the victory celebrated by building Belur temple?", "options": ["Victory over Mughals", "Victory over Cholas", "Victory over Pallavas", "Victory over Rashtrakutas"], "answer": "Victory over Cholas"},
            {"question": "How many sculptures are on the outer walls of Belur temple?", "options": ["200", "400", "600", "800"], "answer": "600"},
            {"question": "What is the platform on which Belur temple sits called?", "options": ["Mandapa", "Jagati", "Shikhara", "Garbhagriha"], "answer": "Jagati"}
        ],
        "halebidu_temple": [
            {"question": "Hoysaleswara Temple is a twin temple dedicated to?", "options": ["Vishnu and Lakshmi", "Shiva and his consort", "Brahma and Saraswati", "Ram and Sita"], "answer": "Shiva and his consort"},
            {"question": "How many elephants are carved on the base of Halebidu temple?", "options": ["120", "180", "240", "300"], "answer": "240"},
            {"question": "Which dynasty built Halebidu temple?", "options": ["Chalukya", "Rashtrakuta", "Hoysala", "Chola"], "answer": "Hoysala"},
            {"question": "What is unique about Halebidu temple compared to most Hindu temples?", "options": ["It has no walls", "It has no tower", "It has no pillars", "It has no roof"], "answer": "It has no tower"},
            {"question": "Halebidu temple is a tentative UNESCO site in which country?", "options": ["Sri Lanka", "Nepal", "India", "Bangladesh"], "answer": "India"}
        ],
        "chitradurga_fort": [
            {"question": "How many secret entrances does Chitradurga Fort have?", "options": ["9", "14", "19", "24"], "answer": "19"},
            {"question": "What does Chitradurga mean in Kannada?", "options": ["Stone city", "Rocky city", "Ancient city", "Golden city"], "answer": "Rocky city"},
            {"question": "Who later expanded Chitradurga Fort?", "options": ["Akbar and Jahangir", "Hyder Ali and Tipu Sultan", "Shivaji and Sambhaji", "Krishna and Rama"], "answer": "Hyder Ali and Tipu Sultan"},
            {"question": "How many bastions protect the walls of Chitradurga Fort?", "options": ["18", "28", "38", "48"], "answer": "38"},
            {"question": "How large is the area enclosed by Chitradurga Fort?", "options": ["500 acres", "1000 acres", "1500 acres", "2000 acres"], "answer": "1500 acres"}
        ],
        "gomateshwara": [
            {"question": "How tall is the Gomateshwara statue?", "options": ["37 feet", "47 feet", "57 feet", "67 feet"], "answer": "57 feet"},
            {"question": "Where is the Gomateshwara statue located?", "options": ["Hampi", "Belur", "Shravanabelagola", "Badami"], "answer": "Shravanabelagola"},
            {"question": "The Gomateshwara statue is carved from?", "options": ["Marble", "Sandstone", "Granite", "Limestone"], "answer": "Granite"},
            {"question": "How often is the Mahamastakabhisheka ceremony held?", "options": ["Every 4 years", "Every 8 years", "Every 12 years", "Every 16 years"], "answer": "Every 12 years"},
            {"question": "From how far away is the Gomateshwara statue visible?", "options": ["10 km", "20 km", "30 km", "40 km"], "answer": "30 km"}
        ],
        "pattadakal": [
            {"question": "How many temples are there at Pattadakal?", "options": ["6", "8", "10", "12"], "answer": "10"},
            {"question": "When did Pattadakal become a UNESCO World Heritage Site?", "options": ["1977", "1982", "1987", "1992"], "answer": "1987"},
            {"question": "Pattadakal was used as the coronation site of which dynasty?", "options": ["Hoysala", "Chalukya", "Rashtrakuta", "Vijayanagara"], "answer": "Chalukya"},
            {"question": "How many of the Pattadakal temples are Hindu?", "options": ["7", "8", "9", "10"], "answer": "9"},
            {"question": "The Virupaksha temple at Pattadakal was built to celebrate victory over?", "options": ["Cholas", "Pallavas", "Rashtrakutas", "Mughals"], "answer": "Pallavas"}
        ],
        "aihole_temples": [
            {"question": "How many ancient temples are in Aihole?", "options": ["50", "80", "120", "150"], "answer": "120"},
            {"question": "What is Aihole called?", "options": ["Cradle of Indian art", "Cradle of Indian temple architecture", "Cradle of Indian culture", "Cradle of Indian music"], "answer": "Cradle of Indian temple architecture"},
            {"question": "Aihole was the first capital of which dynasty?", "options": ["Hoysala dynasty", "Rashtrakuta dynasty", "Chalukya dynasty", "Nayaka dynasty"], "answer": "Chalukya dynasty"},
            {"question": "The Durga temple at Aihole has a plan similar to?", "options": ["Hindu mandirs", "Buddhist chaityas", "Jain basadis", "Muslim mosques"], "answer": "Buddhist chaityas"},
            {"question": "Some temples in Aihole date back to which century?", "options": ["1st century CE", "2nd century CE", "3rd century CE", "4th century CE"], "answer": "4th century CE"}
        ],
    }

    questions = all_quizzes.get(landmark_name, all_quizzes['taj_mahal'])
    return jsonify({
        'landmark': landmark_name,
        'questions': questions
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)