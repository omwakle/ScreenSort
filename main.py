import os
import shutil
import pytesseract
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image



# Update the path to match your Tesseract installation directory
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'  # For Windows




# Path Configurations
screenshot_folder = r"C:/Users/parth/OneDrive/Pictures/Screenshots"
output_folder = r"C:/Users/parth/OneDrive/Pictures"
# Ensure category folders exist
categories = ["Work", "Social Media", "Study"]
for category in categories:
    os.makedirs(os.path.join(output_folder, category), exist_ok=True)

# Function to categorize based on keywords
def categorize_screenshot(text):
    if any(keyword in text.lower() for keyword in ["email", "report", "meeting"]):
        return "Work"
    elif any(keyword in text.lower() for keyword in ["facebook", "twitter", "instagram"]):
        return "Social Media"
    elif any(keyword in text.lower() for keyword in ["lecture", "assignment", "notes"]):
        return "Study"
    return "Uncategorized"

# Handler for new files
class ScreenshotHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith((".png", ".jpg")):
            return

        print(f"New screenshot detected: {event.src_path}")
        try:
            # Extract text from the image
            image = Image.open(event.src_path)
            text = pytesseract.image_to_string(image)

            # Categorize based on extracted text
            category = categorize_screenshot(text)
            category_path = os.path.join(output_folder, category)

            # Move file to the categorized folder
            shutil.move(event.src_path, os.path.join(category_path, os.path.basename(event.src_path)))
            print(f"Moved screenshot to: {category_path}")

        except Exception as e:
            print(f"Error processing file {event.src_path}: {e}")

# Monitor the folder
observer = Observer()
event_handler = ScreenshotHandler()
observer.schedule(event_handler, screenshot_folder, recursive=False)
observer.start()

print(f"Monitoring {screenshot_folder} for new screenshots...")

try:
    while True:
        pass  # Keep the script running
except KeyboardInterrupt:
    observer.stop()
observer.join()
