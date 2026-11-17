
import torch
import torch.nn as nn

from transformers import pipeline
from torchvision import models, transforms
from PIL import Image


# ==========================================
# 1. LOAD CLIP FOOD DETECTOR
# ==========================================

print("\nLoading FoodSaver AI...")
print("Loading CLIP Food Detector...")

food_detector = pipeline(
    "zero-shot-image-classification",
    model="openai/clip-vit-base-patch32",
    device=-1
)

print("CLIP Food Detector Ready!")


# Supported food categories

FRUIT_LABEL = "a photo of a fruit"

VEGETABLE_LABEL = "a photo of a vegetable"

SUPPORTED_FOOD_LABELS = [
    FRUIT_LABEL,
    VEGETABLE_LABEL
]


# CLIP candidate labels

candidate_labels = [
    FRUIT_LABEL,
    VEGETABLE_LABEL,

    "a photo of a cooked meal",
    "a photo of a burger or sandwich",
    "a photo of pizza",
    "a photo of cooked meat",
    "a photo of bread or bakery food",

    "a photo of a driving licence or identity card",
    "a photo of a document or paper",
    "a photo of a person",
    "a photo of an animal",
    "a photo of a mobile phone",
    "a photo of a computer",
    "a photo of a vehicle",
    "a photo of furniture",
    "a photo of a building or landscape",
    "a photo of a logo or graphic design",
    "a photo of an unrelated object"
]


# ==========================================
# 2. LOAD TRAINED MOBILENET MODEL
# ==========================================

device = torch.device("cpu")

MODEL_PATH = "food_model.pth"

print("\nLoading MobileNetV3 Model...")

checkpoint = torch.load(
    MODEL_PATH,
    map_location=device,
    weights_only=False
)

class_names = checkpoint["class_names"]

IMAGE_SIZE = checkpoint["image_size"]


# Recreate MobileNetV3-Small

model = models.mobilenet_v3_small(
    weights=None
)

input_features = model.classifier[3].in_features

model.classifier[3] = nn.Linear(
    input_features,
    len(class_names)
)


# Load trained weights

model.load_state_dict(
    checkpoint["model_state_dict"]
)

model = model.to(device)

model.eval()

print("FoodSaver AI Model Loaded Successfully!")


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
# 4. FOOD ANALYSIS FUNCTION
# ==========================================

def analyze_food(image_path):

    image = Image.open(
        image_path
    ).convert("RGB")


    # --------------------------------------
    # STAGE 1: FOOD / NON-FOOD DETECTION
    # --------------------------------------

    print("\nStarting CLIP Food Detection...")

    food_check = food_detector(
        image,
        candidate_labels=candidate_labels
    )


    print("\n========== CLIP DETECTION RESULTS ==========")

    for item in food_check:

        print(
            f"{item['label']} : "
            f"{item['score'] * 100:.2f}%"
        )

    print("============================================")


    # Check top CLIP prediction

    detected_category = food_check[0]["label"]


    if detected_category not in SUPPORTED_FOOD_LABELS:

        print("\nUnsupported Food / Non-Food Image Detected!")

        return {

            "label": "Unsupported Image",

            "food": "Unknown",

            "freshness": "N/A",

            "confidence": 0,

            "predictions": [],

            "is_food": False

        }


    print("\nSupported Food Image Detected!")


    # --------------------------------------
    # STAGE 2: MOBILENET FOOD ANALYSIS
    # --------------------------------------

    print("\nStarting MobileNet Freshness Analysis...")


    image_tensor = preprocess(
        image
    ).unsqueeze(0)

    image_tensor = image_tensor.to(device)


    with torch.no_grad():

        outputs = model(image_tensor)

        probabilities = torch.softmax(
            outputs,
            dim=1
        )


        # Get Top 5 Predictions

        top_k = min(5, len(class_names))

        top_probabilities, top_indices = torch.topk(
            probabilities,
            k=top_k,
            dim=1
        )


    # --------------------------------------
    # STAGE 3: PREPARE PREDICTIONS
    # --------------------------------------

    confidence = top_probabilities[0][0]

    predicted = top_indices[0][0]


    predictions = []

    for i in range(top_k):

        predictions.append({

            "label": class_names[
                top_indices[0][i].item()
            ],

            "score": top_probabilities[0][i].item()

        })


    # --------------------------------------
    # STAGE 4: IDENTIFY FOOD AND FRESHNESS
    # --------------------------------------

    label = class_names[
        predicted.item()
    ]


    confidence_score = confidence.item() * 100


    if label.startswith("Fresh"):

        freshness = "Fresh"

        food = label.replace(
            "Fresh", ""
        )


    elif label.startswith("Rotten"):

        freshness = "Rotten"

        food = label.replace(
            "Rotten", ""
        )


    else:

        freshness = "Unknown"

        food = label


    # --------------------------------------
    # STAGE 5: FINAL RESULT
    # --------------------------------------

    result = {

        "label": label,

        "food": food,

        "freshness": freshness,

        "confidence": round(
            confidence_score, 2
        ),

        "predictions": predictions,

        "is_food": True

    }


    print("\n========== FOOD ANALYSIS RESULT ==========")

    print("Food:", food)

    print("Freshness:", freshness)

    print(
        "Confidence:",
        round(confidence_score, 2),
        "%"
    )

    print("===========================================")


    return result


# ==========================================
# FOOD MODEL READY
# ==========================================

print("\n================================")

print("FoodSaver AI Ready!")

print("CLIP Food Detection: Active")

print("MobileNet Freshness Model: Active")

print("================================")
