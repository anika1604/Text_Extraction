import cv2
import numpy as np
import imutils
import pytesseract

# Set path for Tesseract-OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def detect_document(image_path):
    """Detects the largest document-like contour in the image."""
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Error: Cannot open image file '{image_path}'. Check the file path!")

    orig = image.copy()
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5,5),0)
    
    # Detect edges using Canny
    edged = cv2.Canny(blurred, 50, 150)

    # Find contours
    contours = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    
    # Sort by largest contour
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    doc_contour = None  # Initialize contour

    for contour in contours:
        peri = cv2.arcLength(contour, True)  # Perimeter
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)  # Approximate shape

        if len(approx) == 4:  # Paper should have 4 corners
            doc_contour = approx
            break
    
    if doc_contour is None:
        raise ValueError("Error: No document detected. Try using a clearer image.")

    return orig, doc_contour

def warp_perspective(image, doc_contour):
    """Applies a perspective transform to get a top-down view of the document."""
    doc_contour = doc_contour.reshape(4, 2)

    # Get ordered points
    rect = np.zeros((4, 2), dtype="float32")
    s = doc_contour.sum(axis=1)
    diff = np.diff(doc_contour, axis=1)

    rect[0] = doc_contour[np.argmin(s)]  # Top-left
    rect[2] = doc_contour[np.argmax(s)]  # Bottom-right
    rect[1] = doc_contour[np.argmin(diff)]  # Top-right
    rect[3] = doc_contour[np.argmax(diff)]  # Bottom-left

    (tl, tr, br, bl) = rect

    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped

def extract_text(image):
    """Extracts text from the preprocessed document image using OCR."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    text = pytesseract.image_to_string(thresh, lang='eng')

    return text

# ==== Run the pipeline ====
image_path = "img3.png"  # Ensure this is correct or use the absolute path

try:
    original, bounding_box = detect_document(image_path)
    warped_image = warp_perspective(original, bounding_box)
    extracted_text = extract_text(warped_image)

    # Show results
    cv2.imshow("Original with Bounding Box", original)
    cv2.imshow("Warped Document", warped_image)

    print("\n===== Extracted Text =====\n")
    print(extracted_text)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
except Exception as e:
    print(e)
