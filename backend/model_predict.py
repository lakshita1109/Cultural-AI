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

# ── LANDMARK INFO DATABASE ──
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
        'culture': 'Red Fort is a symbol of India\'s rich Mughal heritage and national pride. Every Independence Day, the Prime Minister addresses the nation from here.'
    },
    'qutub_minar': {
        'name': 'Qutub Minar',
        'location': 'Delhi, India',
        'history': 'Qutub Minar was built in 1193 by Qutub-ud-din Aibak, the founder of the Delhi Sultanate. It is the world\'s tallest brick minaret.',
        'facts': [
            'Qutub Minar is 72.5 metres tall.',
            'It has 379 steps inside.',
            'It was built in stages by different rulers.',
            'The Iron Pillar nearby has not rusted in 1600 years.',
            'It became a UNESCO World Heritage Site in 1993.'
        ],
        'culture': 'Qutub Minar represents the beginning of Islamic architecture in India and marks an important turning point in Indian history.'
    },
    'india_gate': {
        'name': 'India Gate',
        'location': 'New Delhi, India',
        'history': 'India Gate was built in 1931 as a war memorial to honor 70,000 Indian soldiers who died in World War I and the Afghan Wars.',
        'facts': [
            'India Gate is 42 metres tall.',
            'It was designed by Sir Edwin Lutyens.',
            'Names of 13,300 soldiers are inscribed on it.',
            'The Amar Jawan Jyoti flame burns continuously since 1972.',
            'It is one of the largest war memorials in India.'
        ],
        'culture': 'India Gate is a symbol of national pride and sacrifice. It is a popular gathering place for citizens and tourists alike.'
    },
    'charminar': {
        'name': 'Charminar',
        'location': 'Hyderabad, Telangana, India',
        'history': 'Charminar was built in 1591 by Muhammad Quli Qutb Shah to celebrate the end of a deadly plague and the founding of Hyderabad city.',
        'facts': [
            'Charminar means Four Minarets in Urdu.',
            'Each minaret is 56 metres tall.',
            'It was built to mark the end of a plague epidemic.',
            'There is a mosque on the top floor.',
            'It is surrounded by one of the largest bazaars in India.'
        ],
        'culture': 'Charminar is the icon of Hyderabad and represents the city\'s rich Islamic architectural heritage and its blend of cultures.'
    }
}

# ── PREDICT FUNCTION ──
def predict_landmark(image_path):
    # Open and transform image
    image = Image.open(image_path).convert('RGB')
    image_tensor = transform(image).unsqueeze(0)

    # Run through model
    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        confidence, predicted_idx = torch.max(probabilities, 0)

    # Get predicted class
    predicted_class = class_names[predicted_idx.item()]
    confidence_percent = round(confidence.item() * 100, 1)

    # Get landmark info
    info = landmark_info.get(predicted_class, {})

    return {
        'landmark': info.get('name', predicted_class),
        'confidence': confidence_percent,
        'location': info.get('location', 'Unknown'),
        'history': info.get('history', ''),
        'facts': info.get('facts', []),
        'culture': info.get('culture', '')
    }