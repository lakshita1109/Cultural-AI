import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'saved_model', 'landmark_model.pth')
CLASS_NAMES_PATH = os.path.join(BASE_DIR, 'model', 'saved_model', 'class_names.json')

with open(CLASS_NAMES_PATH, 'r') as f:
    class_names = json.load(f)

model = models.resnet18(weights=None)
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, len(class_names))
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# Test with an image - change this path to your hampi image
image_path = sys.argv[1]
image = Image.open(image_path).convert('RGB')
image_tensor = transform(image).unsqueeze(0)

with torch.no_grad():
    outputs = model(image_tensor)
    probabilities = torch.nn.functional.softmax(outputs[0], dim=0)

print("\nAll predictions:")
for i, (prob, name) in enumerate(zip(probabilities, class_names)):
    print(f"{name}: {prob.item()*100:.1f}%")