
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from food_model import analyze_food
from food_tips import get_food_tips

from PIL import Image, UnidentifiedImageError

import os
import uuid
import sqlite3
from datetime import datetime


# =====================================
# 1. FLASK APPLICATION
# =====================================

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(
    BASE_DIR, "static", "uploads"
)

DATABASE = os.path.join(
    BASE_DIR, "foodsaver.db"
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}


# =====================================
# 2. DATABASE CONNECTION
# =====================================

def get_db_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


# =====================================
# 3. CREATE DATABASE TABLE
# =====================================

def initialize_database():

    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS food_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            image_name TEXT NOT NULL,

            food TEXT,

            freshness TEXT,

            confidence REAL DEFAULT 0,

            is_food INTEGER DEFAULT 0,

            created_at TEXT NOT NULL

        )
    """)

    conn.commit()
    conn.close()

    print("FoodSaver AI Database Ready!")


# =====================================
# 4. SAVE ANALYSIS RESULT
# =====================================

def save_analysis(image_name, result):

    conn = get_db_connection()

    conn.execute("""
        INSERT INTO food_history (

            image_name,
            food,
            freshness,
            confidence,
            is_food,
            created_at

        )

        VALUES (?, ?, ?, ?, ?, ?)

    """, (

        image_name,
        result.get("food", "Unknown"),
        result.get("freshness", "N/A"),
        result.get("confidence", 0),
        1 if result.get("is_food") else 0,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ))

    conn.commit()
    conn.close()

    print("Analysis Saved Successfully!")


# =====================================
# 5. FILE VALIDATION
# =====================================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# =====================================
# 6. HOME PAGE
# =====================================

@app.route("/")
def home():

    return render_template("index.html")


# =====================================
# 7. FOOD IMAGE ANALYSIS
# =====================================

@app.route("/analyze", methods=["POST"])
def analyze():

    if "food_image" not in request.files:

        return "No image selected!", 400

    file = request.files["food_image"]

    if file.filename == "":

        return "Please select an image!", 400

    if not allowed_file(file.filename):

        return "Please upload a valid image!", 400

    filename = secure_filename(file.filename)

    extension = filename.rsplit(".", 1)[1].lower()

    unique_filename = f"{uuid.uuid4().hex}.{extension}"

    image_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        unique_filename
    )

    try:

        # Save image

        file.save(image_path)

        # Validate actual image

        with Image.open(image_path) as img:

            img.verify()

        print("\nStarting FoodSaver AI Analysis...")

        # AI Recognition

        result = analyze_food(image_path)

        print("Food:", result.get("food"))
        print("Freshness:", result.get("freshness"))
        print("Confidence:", result.get("confidence"))

        # Save analysis to database

        save_analysis(unique_filename, result)

        # Food Storage Tips

        tips = None

        if result.get("is_food"):

            tips = get_food_tips(
                result["label"]
            )

        # Display Results

        return render_template(
            "result.html",
            image_name=unique_filename,
            result=result,
            tips=tips
        )

    except UnidentifiedImageError:

        if os.path.exists(image_path):
            os.remove(image_path)

        return (
            "Invalid image file. Please upload a real image.",
            400
        )

    except Exception as e:

        print("Analysis Error:", e)

        return (
            "Something went wrong during AI analysis!",
            500
        )


# =====================================
# 8. ADMIN DASHBOARD
# =====================================

@app.route("/admin")
def admin():

    conn = get_db_connection()

    # ---------------------------------
    # TOTAL IMAGES
    # ---------------------------------

    total_scans = conn.execute("""
        SELECT COUNT(*)
        FROM food_history
    """).fetchone()[0]


    # ---------------------------------
    # FRESH FOOD
    # ---------------------------------

    fresh_count = conn.execute("""
        SELECT COUNT(*)
        FROM food_history
        WHERE is_food = 1
        AND freshness = 'Fresh'
    """).fetchone()[0]


    # ---------------------------------
    # ROTTEN FOOD
    # ---------------------------------

    rotten_count = conn.execute("""
        SELECT COUNT(*)
        FROM food_history
        WHERE is_food = 1
        AND freshness = 'Rotten'
    """).fetchone()[0]


    # ---------------------------------
    # NON-FOOD IMAGES
    # ---------------------------------

    non_food_count = conn.execute("""
        SELECT COUNT(*)
        FROM food_history
        WHERE is_food = 0
    """).fetchone()[0]


    # ---------------------------------
    # RECENT ANALYSIS HISTORY
    # ---------------------------------

    recent_records = conn.execute("""
        SELECT *
        FROM food_history
        ORDER BY id DESC
        LIMIT 10
    """).fetchall()


    # ---------------------------------
    # FOOD CATEGORY STATISTICS
    # ---------------------------------

    food_stats = [
        dict(row) for row in conn.execute("""
            SELECT
                food,
                COUNT(*) AS total

            FROM food_history

            WHERE is_food = 1

            GROUP BY food

            ORDER BY total DESC

        """).fetchall()
    ]


    # ---------------------------------
    # MONTHLY ANALYSIS STATISTICS
    # ---------------------------------

    monthly_stats = [
        dict(row) for row in conn.execute("""
            SELECT

                SUBSTR(created_at, 1, 7) AS month,

                COUNT(*) AS total

            FROM food_history

            GROUP BY SUBSTR(created_at, 1, 7)

            ORDER BY month ASC

        """).fetchall()
    ]


    # ---------------------------------
    # CLOSE DATABASE
    # ---------------------------------

    conn.close()


    # ---------------------------------
    # SEND DATA TO ADMIN.HTML
    # ---------------------------------

    return render_template(

        "admin.html",

        total_scans=total_scans,

        fresh_count=fresh_count,

        rotten_count=rotten_count,

        non_food_count=non_food_count,

        recent_records=recent_records,

        food_stats=food_stats,

        monthly_stats=monthly_stats

    )


# =====================================
# 9. FILE SIZE ERROR
# =====================================

@app.errorhandler(413)
def file_too_large(error):

    return (
        "Image is too large. Maximum size is 5 MB.",
        413
    )


# =====================================
# 10. INITIALIZE DATABASE
# =====================================

initialize_database()


# =====================================
# 11. RUN APPLICATION
# =====================================

if __name__ == "__main__":

    app.run(debug=True)
