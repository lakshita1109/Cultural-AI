# ── IMPORTS ──
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split
import os
import json
import matplotlib.pyplot as plt

# ── SETTINGS ──
DATA_DIR = 'data'
MODEL_DIR = 'model/saved_model'
BATCH_SIZE = 8
EPOCHS = 15
LEARNING_RATE = 0.001
IMG_SIZE = 224

os.makedirs(MODEL_DIR, exist_ok=True)

# ── STEP 1: PREPARE IMAGES ──
# Transform = resize, normalize images so model can process them
train_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.RandomHorizontalFlip(),     # flip image randomly (more variety)
    transforms.RandomRotation(10),         # rotate slightly (more variety)
    transforms.ColorJitter(brightness=0.2),# change brightness slightly
    transforms.ToTensor(),                 # convert to numbers
    transforms.Normalize(                  # normalize pixel values
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

val_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ── STEP 2: LOAD DATASET ──
print("Loading dataset...")
full_dataset = datasets.ImageFolder(root=DATA_DIR, transform=train_transform)

# Get class names (landmark names)
class_names = full_dataset.classes
print(f"Classes found: {class_names}")
print(f"Total images: {len(full_dataset)}")

# Save class names so Flask can use them later
with open(os.path.join(MODEL_DIR, 'class_names.json'), 'w') as f:
    json.dump(class_names, f)
print("Class names saved!")

# ── STEP 3: SPLIT INTO TRAIN AND VALIDATION ──
# 80% for training, 20% for testing accuracy
train_size = int(0.8 * len(full_dataset))
val_size = len(full_dataset) - train_size
train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])

# Apply different transform to validation set
val_dataset.dataset.transform = val_transform

print(f"Training images: {train_size}")
print(f"Validation images: {val_size}")

# ── STEP 4: CREATE DATA LOADERS ──
# DataLoader feeds images to model in batches
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

# ── STEP 5: LOAD PRETRAINED MODEL ──
print("Loading pretrained ResNet18 model...")
# ResNet18 is already trained on millions of images
# We just replace its last layer to recognize our 5 landmarks
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

# Freeze all layers except last one
# This means we only train the last layer
for param in model.parameters():
    param.requires_grad = False

# Replace last layer with our own (5 classes)
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, len(class_names))

print(f"Model ready! Output classes: {len(class_names)}")

# ── STEP 6: SET UP TRAINING ──
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Training on: {device}")

model = model.to(device)

# Loss function — measures how wrong the model is
criterion = nn.CrossEntropyLoss()

# Optimizer — adjusts model weights to reduce loss
optimizer = optim.Adam(model.fc.parameters(), lr=LEARNING_RATE)

# ── STEP 7: TRAINING LOOP ──
print("\nStarting training...")
train_losses = []
val_accuracies = []

for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0

    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)

        # Clear previous gradients
        optimizer.zero_grad()

        # Forward pass — model makes prediction
        outputs = model(images)

        # Calculate loss — how wrong was the prediction
        loss = criterion(outputs, labels)

        # Backward pass — calculate how to improve
        loss.backward()

        # Update model weights
        optimizer.step()

        running_loss += loss.item()

    # ── VALIDATION ──
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total
    avg_loss = running_loss / len(train_loader)

    train_losses.append(avg_loss)
    val_accuracies.append(accuracy)

    print(f"Epoch {epoch+1}/{EPOCHS} | Loss: {avg_loss:.4f} | Accuracy: {accuracy:.1f}%")

# ── STEP 8: SAVE THE MODEL ──
model_path = os.path.join(MODEL_DIR, 'landmark_model.pth')
torch.save(model.state_dict(), model_path)
print(f"\nModel saved to {model_path}")

# ── STEP 9: SAVE ACCURACY GRAPH ──
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.plot(train_losses, color='coral')
plt.title('Training Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')

plt.subplot(1, 2, 2)
plt.plot(val_accuracies, color='teal')
plt.title('Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy %')

plt.tight_layout()
plt.savefig(os.path.join(MODEL_DIR, 'training_graph.png'))
print("Training graph saved!")

print(f"\nFinal Accuracy: {val_accuracies[-1]:.1f}%")
print("Training complete!")