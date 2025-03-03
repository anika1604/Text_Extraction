# Text_Extraction

# OCR Text Extraction

This is a web application based on Flask that allows users to upload an image, select a region on the image, and extract text from the selected area using Optical Character Recognition (OCR).

## Features
- Upload an image file for text extraction
- Select a region on the image using a canvas
- Extract text from the selected area using OCR
- View the extracted text in the browser

---

## 🚀 Getting Started

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Pip (Python package manager)
- Flask
- Tesseract OCR

### Installation
1. **Clone the repository:**
   ```sh
   git clone https://github.com/anika1604/Text_Extraction.git
   cd Text_Extraction
   ```

2. **Create a virtual environment (optional but recommended):**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install required dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Install Tesseract OCR**
   - **Windows:** Download and install [Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki)
   - **Linux/macOS:** Install via package manager (e.g., `sudo apt install tesseract-ocr`)

5. **Run the Flask application:**
   ```sh
   python app.py
   ```

6. **Open in Browser:**
   Navigate to `http://127.0.0.1:5000/` in your web browser.

---

## 📌 API Documentation

### 1. Upload Image
- **Endpoint:** `POST /upload`
- **Description:** Accepts an image file and saves it to the server.
- **Request:**
  - Form Data: `image` (file)
- **Response:**
  ```json
  {
    "file_path": "/uploads/image.jpg"
  }
  ```

### 2. Extract Text
- **Endpoint:** `POST /extract_text`
- **Description:** Extracts text from a selected region of the uploaded image.
- **Request:**
  - JSON Body:
    ```json
    {
      "file_path": "/uploads/image.jpg",
      "x1": 10,
      "y1": 20,
      "x2": 200,
      "y2": 300
    }
    ```
- **Response:**
  ```json
  {
    "extracted_text": "Sample extracted text"
  }
  ```

---

## 🛠 Troubleshooting
- **Issue:** `jinja2.exceptions.TemplateNotFound: index.html`
  - **Solution:** Ensure `index.html` is inside the `templates/` folder.
- **Issue:** `tesseract: command not found`
  - **Solution:** Ensure Tesseract is installed and added to system PATH.

---

## 💡 Future Improvements
- Support for multiple image formats
- Download extracted text as a file
- Improved UI/UX

---

## 👨‍💻 Contributing
Feel free to fork this project and submit pull requests!

---

## 📜 License
This project is licensed under the MIT License. See `LICENSE` for details.

---

## 📞 Contact
For any issues or feature requests, contact: `anika1605singhal@gmail.com`

