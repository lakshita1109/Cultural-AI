# Cultural AI

An AI-powered web application that identifies Indian monuments from photos and delivers rich educational content — history, fun facts, cultural significance, and interactive quizzes.

## Features

- **AI Landmark Recognition** — Uses OpenAI CLIP (ViT-B/32) to identify 20+ Indian landmarks from uploaded images with confidence scoring
- **Educational Content** — Detailed history, curated fun facts, and cultural context for each landmark
- **Interactive Quizzes** — 5-question quizzes per landmark to test your knowledge
- **Explore Mode** — Browse all landmarks with cards and discover new places

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask, Flask-CORS |
| AI Model | OpenAI CLIP (ViT-B/32) via zero-shot classification |
| Frontend | Vanilla HTML, CSS, JavaScript |
| Deployment | Heroku (via Procfile) |

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Clone the repo
git clone <repo-url>
cd Cultural-AI

# Install dependencies
pip install -r requirements.txt
```

This installs PyTorch, torchvision, CLIP, Flask, and other required packages.

### Running the App

```bash
python backend/app.py
```

The server starts at `http://localhost:5000`. Open it in your browser, upload a photo of a monument, and the AI will identify it.

### Environment Variables

- `PORT` — Server port (defaults to 5000)

## Project Structure

```
Cultural-AI/
├── backend/
│   ├── app.py             # Flask API — /predict, /quiz/<name>, static frontend
│   ├── clip_predict.py    # CLIP-based landmark recognition (primary model)
│   ├── model_predict.py   # ResNet18-based recognition (secondary model)
│   └── uploads/           # Temporary uploaded images
├── frontend/
│   ├── index.html         # Home — image upload page
│   ├── result.html        # Results — history, facts, culture tabs
│   ├── learn.html         # Explore — landmark cards gallery
│   ├── quiz.html          # Quiz — interactive questions
│   ├── css/               # Stylesheets
│   └── js/                # Client-side logic
├── model/
│   └── train.py           # PyTorch training script for ResNet18
├── requirements.txt       # Python dependencies
├── Procfile               # Heroku deployment
└── test_clip.py           # CLI test for CLIP model
```

## API Endpoints

### `POST /predict`

Upload an image to identify a landmark.

**Request:** `multipart/form-data` with field `image` (jpg, png, webp)

**Response:**
```json
{
  "landmark": "Taj Mahal",
  "confidence": 94.2,
  "location": "Agra, Uttar Pradesh, India",
  "history": "The Taj Mahal was built by...",
  "facts": ["Fact 1", "Fact 2", ...],
  "culture": "Cultural significance..."
}
```

### `GET /quiz/<landmark_name>`

Get a 5-question quiz for a landmark.

**Response:**
```json
{
  "landmark": "taj_mahal",
  "questions": [
    { "question": "...", "options": [...], "answer": "..." },
    ...
  ]
}
```

Landmark keys: `taj_mahal`, `red_fort`, `qutub_minar`, `india_gate`, `charminar`, `hampi`, `lotus_temple`, `ajanta_caves`, `gateway_of_india`, `virupaksha_temple`, `mysore_palace`, `gol_gumbaz`, `badami_caves`, `belur_temple`, `halebidu_temple`, `chitradurga_fort`, `gomateshwara`, `pattadakal`, `aihole_temples`, `bidar_fort`

## Supported Landmarks (20)

| Landmark | Location | Region |
|---|---|---|
| Taj Mahal | Agra, UP | North |
| Red Fort | Delhi | North |
| Qutub Minar | Delhi | North |
| India Gate | New Delhi | North |
| Lotus Temple | New Delhi | North |
| Charminar | Hyderabad | South |
| Hampi | Karnataka | South |
| Virupaksha Temple | Hampi, Karnataka | South |
| Mysore Palace | Mysore, Karnataka | South |
| Gol Gumbaz | Bijapur, Karnataka | South |
| Badami Caves | Karnataka | South |
| Belur Temple | Karnataka | South |
| Halebidu Temple | Karnataka | South |
| Chitradurga Fort | Karnataka | South |
| Gomateshwara Statue | Shravanabelagola, Karnataka | South |
| Pattadakal | Karnataka | South |
| Aihole Temples | Karnataka | South |
| Bidar Fort | Karnataka | South |
| Gateway of India | Mumbai, Maharashtra | West |
| Ajanta Caves | Aurangabad, Maharashtra | West |

## Models

- **Primary (active):** OpenAI CLIP ViT-B/32 — zero-shot classification using cosine similarity between image and text embeddings
- **Secondary (alternative):** Fine-tuned ResNet18 — transfer learning classifier trained with `model/train.py`

Run the CLI tests:
```bash
python test_clip.py <image_path>
python test_model.py <image_path>
```

## Deployment

```bash
# Heroku
heroku create
git push heroku main
```

The `Procfile` starts the Flask server with `python backend/app.py`.
