# FOOD SAVER AI
### AI-Based Food Recognition & Food Waste Management System

**Project Level:** Class XII

## 1. Project Introduction
FoodSaver AI is a web-based application that uses Artificial Intelligence to identify supported fruits and vegetables and classify them as Fresh or Rotten.

## 2. Main Features
- AI-based food image recognition
- Fresh and Rotten food classification
- Food and non-food image screening
- Top 5 prediction results
- Food storage and waste reduction tips
- SQLite database for analysis history
- Admin dashboard with charts

## 3. Technologies Used
- Python
- Flask
- PyTorch
- MobileNetV3-Small
- CLIP
- SQLite
- HTML and CSS
- JavaScript and Chart.js

## 4. How to Run the Project

1. Install Python.
2. Open the project folder in VS Code.
3. Create and activate a virtual environment.
4. Install required libraries:

   `pip install -r requirements.txt`

5. Run the application:

   `python app.py`

6. Open the local URL displayed in the terminal, usually:

   `http://127.0.0.1:5000/`

## 5. Important Files
- app.py – Main Flask application
- food_model.py – AI prediction logic
- food_tips.py – Food storage tips
- food_model.pth – Trained AI model
- foodsaver.db – SQLite database
- requirements.txt – Required Python libraries

## 6. Project Objective
The objective is to demonstrate how Artificial Intelligence can help identify food freshness and encourage better food storage practices to reduce food waste.

## 7. Note
The application supports the food categories included in its trained dataset. Its predictions are not a substitute for professional food-safety inspection.