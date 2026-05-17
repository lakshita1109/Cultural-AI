import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import json
import os

# ── PATHS ──
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'saved_model', 'landmark_model.pth')
CLASS_NAMES_PATH = os.path.join(BASE_DIR, 'model', 'saved_model', 'class_names.json')

# ── LOAD CLASS NAMES ──
with open(CLASS_NAMES_PATH, 'r') as f:
    class_names = json.load(f)

# ── LOAD MODEL ──
model = models.resnet18(weights=None)
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, len(class_names))
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
model.eval()

# ── IMAGE TRANSFORM ──
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ── LANDMARK INFO ──
landmark_info = {
    'taj_mahal': {
        'name': 'Taj Mahal',
        'location': 'Agra, Uttar Pradesh, India',
        'history': 'The Taj Mahal was built by Mughal emperor Shah Jahan between 1632 and 1653 in memory of his beloved wife Mumtaz Mahal. It took over 20,000 artisans to complete.',
        'facts': [
            'The Taj Mahal took 22 years to build.',
            'Over 1000 elephants carried the building materials.',
            'The marble changes color at different times of day.',
            'The four minarets are slightly tilted outward for safety.',
            'It became a UNESCO World Heritage Site in 1983.'
        ],
        'culture': 'The Taj Mahal is a symbol of eternal love and one of India\'s most treasured cultural icons.'
    },
    'red_fort': {
        'name': 'Red Fort',
        'location': 'Delhi, India',
        'history': 'Red Fort was built by Mughal Emperor Shah Jahan in 1639. It served as the main residence of Mughal emperors for nearly 200 years.',
        'facts': [
            'Red Fort took 10 years to build — from 1639 to 1648.',
            'It is made of red sandstone, which gives it its name.',
            'The fort has a perimeter of 2.5 km.',
            'India\'s Prime Minister hoists the flag here every Independence Day.',
            'It became a UNESCO World Heritage Site in 2007.'
        ],
        'culture': 'Red Fort is a symbol of India\'s rich Mughal heritage and national pride.'
    },
    'qutub_minar': {
        'name': 'Qutub Minar',
        'location': 'Delhi, India',
        'history': 'Qutub Minar was built in 1193 by Qutub-ud-din Aibak. It is the world\'s tallest brick minaret at 72.5 metres.',
        'facts': [
            'Qutub Minar is 72.5 metres tall.',
            'It has 379 steps inside.',
            'It was built in stages by different rulers.',
            'The Iron Pillar nearby has not rusted in 1600 years.',
            'It became a UNESCO World Heritage Site in 1993.'
        ],
        'culture': 'Qutub Minar represents the beginning of Islamic architecture in India.'
    },
    'india_gate': {
        'name': 'India Gate',
        'location': 'New Delhi, India',
        'history': 'India Gate was built in 1931 as a war memorial to honor 70,000 Indian soldiers who died in World War I.',
        'facts': [
            'India Gate is 42 metres tall.',
            'It was designed by Sir Edwin Lutyens.',
            'Names of 13,300 soldiers are inscribed on it.',
            'The Amar Jawan Jyoti flame burns continuously since 1972.',
            'It is one of the largest war memorials in India.'
        ],
        'culture': 'India Gate is a symbol of national pride and sacrifice.'
    },
    'charminar': {
        'name': 'Charminar',
        'location': 'Hyderabad, Telangana, India',
        'history': 'Charminar was built in 1591 by Muhammad Quli Qutb Shah to celebrate the end of a deadly plague and the founding of Hyderabad.',
        'facts': [
            'Charminar means Four Minarets in Urdu.',
            'Each minaret is 56 metres tall.',
            'It was built to mark the end of a plague epidemic.',
            'There is a mosque on the top floor.',
            'It is surrounded by one of the largest bazaars in India.'
        ],
        'culture': 'Charminar is the icon of Hyderabad and represents the city\'s rich Islamic architectural heritage.'
    },
    'hampi': {
        'name': 'Hampi',
        'location': 'Hampi, Karnataka, India',
        'history': 'Hampi was the capital of the Vijayanagara Empire in the 14th to 16th centuries. It was one of the largest and richest cities in the world at its peak.',
        'facts': [
            'Hampi was once the second largest city in the world after Beijing.',
            'The ruins spread over 4,100 hectares of land.',
            'Hampi has over 1,600 surviving remains.',
            'It became a UNESCO World Heritage Site in 1986.',
            'The Tungabhadra river flows alongside the ruins.'
        ],
        'culture': 'Hampi represents the golden age of South Indian culture, art and architecture.'
    },
    'lotus_temple': {
        'name': 'Lotus Temple',
        'location': 'New Delhi, India',
        'history': 'The Lotus Temple was built in 1986 and serves as the Bahai House of Worship. It was designed by Iranian architect Fariborz Sahba.',
        'facts': [
            'The Lotus Temple has 27 free-standing marble petals.',
            'It can accommodate up to 2,500 people at a time.',
            'People of all religions are welcome inside.',
            'It has won numerous architectural awards.',
            'It receives over 4 million visitors every year.'
        ],
        'culture': 'The Lotus Temple is a symbol of unity and peace, welcoming people of all faiths.'
    },
    'ajanta_caves': {
        'name': 'Ajanta Caves',
        'location': 'Aurangabad, Maharashtra, India',
        'history': 'The Ajanta Caves are 30 rock-cut Buddhist cave monuments dating from the 2nd century BCE. They contain some of the finest surviving examples of ancient Indian art.',
        'facts': [
            'Ajanta Caves were carved out of solid rock over 2000 years ago.',
            'There are 30 caves in total.',
            'The paintings inside are masterpieces of Buddhist art.',
            'They were rediscovered by a British officer in 1819.',
            'They became a UNESCO World Heritage Site in 1983.'
        ],
        'culture': 'The Ajanta Caves represent the height of ancient Indian artistic achievement.'
    },
    'gateway_of_india': {
        'name': 'Gateway of India',
        'location': 'Mumbai, Maharashtra, India',
        'history': 'The Gateway of India was built in 1924 to commemorate the visit of King George V and Queen Mary to Mumbai in 1911.',
        'facts': [
            'The Gateway of India is 26 metres tall.',
            'It was built in Indo-Saracenic architectural style.',
            'The last British troops left India through this gate in 1948.',
            'It overlooks the Arabian Sea.',
            'It is one of the most visited monuments in India.'
        ],
        'culture': 'The Gateway of India is the iconic symbol of Mumbai and marks the end of British colonial rule in India.'
    }
}

# ── PREDICT FUNCTION ──
def predict_landmark(image_path):
    image = Image.open(image_path).convert('RGB')
    image_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        confidence, predicted_idx = torch.max(probabilities, 0)

    predicted_class = class_names[predicted_idx.item()]
    confidence_percent = round(confidence.item() * 100, 1)

    info = landmark_info.get(predicted_class, {})

    return {
        'landmark': info.get('name', predicted_class),
        'confidence': confidence_percent,
        'location': info.get('location', 'Unknown'),
        'history': info.get('history', ''),
        'facts': info.get('facts', []),
        'culture': info.get('culture', '')
    }