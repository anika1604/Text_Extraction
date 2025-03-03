from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import cv2
import pytesseract
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Serve the frontend UI
@app.route("/")
def index():
    return render_template("index.html")

# # Upload an image and save it
# @app.route("/upload", methods=["POST"])
# def upload_image():
#     if "image" not in request.files:
#         return jsonify({"error": "No file uploaded!"})

#     file = request.files["image"]
#     if file.filename == "":
#         return jsonify({"error": "No selected file!"})

#     file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
#     file.save(file_path)

#     return jsonify({"file_path": f"/uploads/{file.filename}"})

@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        print("🚨 No file uploaded!")
        return jsonify({"error": "No file uploaded!"})

    file = request.files["image"]
    if file.filename == "":
        print("🚨 No selected file!")
        return jsonify({"error": "No selected file!"})

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)
    
    print(f"✅ File saved at: {file_path}")

    return jsonify({"file_path": f"/uploads/{file.filename}"})


# Serve uploaded images
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# Extract text from a selected region
@app.route("/extract_text", methods=["POST"])
def extract_text():
    data = request.json
    file_path = data.get("file_path", "").replace("/uploads/", "")

    x1, y1, x2, y2 = data["x1"], data["y1"], data["x2"], data["y2"]
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], file_path)

    if not os.path.exists(image_path):
        return jsonify({"error": "File not found!"})

    image = cv2.imread(image_path)
    cropped_image = image[y1:y2, x1:x2]

    # Convert image to grayscale for better OCR accuracy
    gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

    # Use Tesseract to extract text
    extracted_text = pytesseract.image_to_string(gray)

    return jsonify({"extracted_text": extracted_text.strip()})

if __name__ == "__main__":
    app.run(debug=True)
