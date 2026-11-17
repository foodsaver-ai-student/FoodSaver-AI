
import os
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

# ==========================================
# 1. CPU MEMORY OPTIMIZATION
# ==========================================

torch.set_num_threads(1)
device = torch.device("cpu")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "food_model.pth")

print("\nLoading FoodSaver AI...")
print("Loading MobileNetV3-Small model...")

# ==========================================
# 2. LOAD TRAINED MODEL
# ==========================================

checkpoint = torch.load(
    MODEL_PATH,
    map_location=device,
    weights_only=False
)

class_names = checkpoint["class_names"]
IMAGE_SIZE = checkpoint["image_size"]

model = models.mobilenet_v3_small(weights=None)

input_features = model.classifier[3].in_features

model.classifier[3] = nn.Linear(
    input_features,
    len(class_names)
)

model.load_state_dict(checkpoint["model_state_dict"])

model = model.to(device)
model.eval()

print("MobileNetV3-Small Loaded Successfully!")

# ==========================================
# 3. IMAGE PREPROCESSING
# ==========================================

preprocess = transforms.Compose([
    transforms.Resize(180),
    transforms.CenterCrop(IMAGE_SIZE),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])

# ==========================================
# 4. FOOD ANALYSIS
# ==========================================

def analyze_food(image_path):

    with Image.open(image_path) as img:
        image = img.convert("RGB")

    image_tensor = preprocess(image).unsqueeze(0)

    with torch.inference_mode():

        outputs = model(image_tensor)

        probabilities = torch.softmax(outputs, dim=1)

        top_k = min(5, len(class_names))

        top_probabilities, top_indices = torch.topk(
            probabilities,
            k=top_k,
            dim=1
        )

    confidence = top_probabilities[0][0].item() * 100

    predicted_index = top_indices[0][0].item()

    label = class_names[predicted_index]

    predictions = []

    for i in range(top_k):

        predictions.append({
            "label": class_names[top_indices[0][i].item()],
            "score": top_probabilities[0][i].item()
        })

    if label.startswith("Fresh"):

        freshness = "Fresh"
        food = label.replace("Fresh", "")

    elif label.startswith("Rotten"):

        freshness = "Rotten"
        food = label.replace("Rotten", "")

    else:

        freshness = "Unknown"
        food = label

    result = {
        "label": label,
        "food": food,
        "freshness": freshness,
        "confidence": round(confidence, 2),
        "predictions": predictions,
        "is_food": True
    }

    print("\n========== FOOD ANALYSIS ==========")
    print("Food:", food)
    print("Freshness:", freshness)
    print("Confidence:", round(confidence, 2), "%")
    print("===================================")

    return result


print("\n================================")
print("FoodSaver AI Ready!")
print("MobileNet Freshness Model: Active")
print("CLIP Detector: Disabled")
print("================================")
