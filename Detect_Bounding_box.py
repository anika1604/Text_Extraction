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

# Perform OCR with bounding box extraction
custom_config = r'--oem 3 --psm 6'  # OCR Engine Mode 3, Page Segmentation Mode 6
data = pytesseract.image_to_data(cleaned, config=custom_config, output_type=pytesseract.Output.DICT)

# Get coordinates of detected words to draw a **single bounding box**
x_min, y_min = np.inf, np.inf
x_max, y_max = 0, 0

text_blocks = []

for i in range(len(data['text'])):
    if data['text'][i].strip():  # Ignore empty text
        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
        x_min, y_min = min(x_min, x), min(y_min, y)
        x_max, y_max = max(x_max, x + w), max(y_max, y + h)

        # Store words along with their positions for proper ordering
        text_blocks.append((data['block_num'][i], data['par_num'][i], data['line_num'][i], data['word_num'][i], data['text'][i]))

# **Sort text based on block, paragraph, line, and word order**
text_blocks.sort()

# Reconstruct text in correct order
extracted_text = ""
current_line = -1
for block, para, line, word, text in text_blocks:
    if line != current_line:
        extracted_text += "\n"  # Add new line when moving to a new line in document
        current_line = line
    extracted_text += " " + text

# Draw **one bounding box** around the full text region
if x_min < np.inf and y_min < np.inf:  # Ensure at least one text block is detected
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)  # Green bounding box

# Display the image with the bounding box
cv2.imshow("Text Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save extracted text to a file
output_file = "extracted_text.txt"
with open(output_file, "w", encoding="utf-8") as file:
    file.write(extracted_text.strip())

print(f"Extracted text saved to {output_file}")
