import os
import pytesseract
from PIL import Image
import shutil
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# Step 1: Capture Screenshot (for the purpose of this example, we assume a screenshot is already captured)
screenshot_path = "C:/Users/parth/OneDrive/Pictures/Screenshots/Screenshot (1154).png"
screenshot = Image.open(screenshot_path)

# Step 2: Extract text using OCR (Tesseract)
extracted_text = pytesseract.image_to_string(screenshot)
print(f"Extracted Text: {extracted_text}")

# Step 3: Analyze the extracted text and determine the category
def categorize_text(text):
    if 'invoice' in text.lower():
        return 'Invoices'
    elif 'meeting' in text.lower():
        return 'Meetings'
    elif 'report' in text.lower():
        return 'Reports'
    else:
        return 'Miscellaneous'

category = categorize_text(extracted_text)
print(f"Category: {category}")

# Step 4: Create the folder if it doesn't exist
def create_or_get_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

folder = create_or_get_folder(category)

# Step 5: Move the screenshot to the categorized folder
def move_screenshot_to_folder(screenshot_path, folder_name):
    shutil.move(screenshot_path, os.path.join(folder_name, os.path.basename(screenshot_path)))

move_screenshot_to_folder(screenshot_path, folder)

print(f"Screenshot moved to {folder} folder.")
