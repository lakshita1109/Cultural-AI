from backend.clip_predict import predict_landmark
import sys

image_path = sys.argv[1]
print(f"Testing: {image_path}")
result = predict_landmark(image_path)
print(f"Landmark: {result['landmark']}")
print(f"Confidence: {result['confidence']}%")
print(f"Location: {result['location']}")