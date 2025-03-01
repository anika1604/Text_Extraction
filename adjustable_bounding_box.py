import cv2
import pytesseract
import numpy as np

# Load image
image_path = "img3.png"
image = cv2.imread(image_path)

# Convert to grayscale and apply adaptive thresholding
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# Remove noise using morphological operations
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# Variables for bounding box selection
x1, y1, x2, y2 = 0, 0, 0, 0
drawing = False  # To track if the user is drawing a bounding box

# Mouse callback function
def draw_rectangle(event, x, y, flags, param):
    global x1, y1, x2, y2, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        # Start drawing
        drawing = True
        x1, y1 = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            x2, y2 = x, y  # Update rectangle while dragging

    elif event == cv2.EVENT_LBUTTONUP:
        # Stop drawing
        drawing = False
        x2, y2 = x, y  # Finalize rectangle

# Display adjustable bounding box
cv2.namedWindow("Adjust Bounding Box")
cv2.setMouseCallback("Adjust Bounding Box", draw_rectangle)

while True:
    temp_image = image.copy()
    
    if x1 != x2 and y1 != y2:  # Draw rectangle only if it exists
        cv2.rectangle(temp_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow("Adjust Bounding Box", temp_image)
    
    key = cv2.waitKey(1) & 0xFF
    if key == 13:  # Press 'Enter' to finalize selection
        break

cv2.destroyAllWindows()

# Ensure valid bounding box coordinates
x1, x2 = min(x1, x2), max(x1, x2)
y1, y2 = min(y1, y2), max(y1, y2)

# Crop the selected region
roi = cleaned[y1:y2, x1:x2]

# Perform OCR on the selected region
custom_config = r'--oem 3 --psm 6'
extracted_text = pytesseract.image_to_string(roi, config=custom_config)

# Save extracted text to a file
output_file = "extracted_text.txt"
with open(output_file, "w", encoding="utf-8") as file:
    file.write(extracted_text.strip())

print(f"Extracted text saved to {output_file}")
print("Extracted Text:\n", extracted_text.strip())
