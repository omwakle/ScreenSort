import os
import shutil
import pytesseract
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image
from groq import Groq
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    filename='screenshot_categorization.log'
)

# Path Configurations
screenshot_folder = r"C:/Users/parth/OneDrive/Pictures/Screenshots"
output_folder = r"C:/Users/parth/OneDrive/Pictures/Organized Screenshots"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Groq API Configuration
try:
    # Recommend using environment variable for API key
    groq_client = Groq(api_key="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")
except Exception as e:
    logging.error(f"Groq API Initialization Error: {e}")
    raise

def categorize_screenshot_with_groq(text):
    """
    Categorize screenshot using Groq API with advanced prompt engineering
    
    Args:
        text (str): OCR extracted text from screenshot
    
    Returns:
        str: Categorized folder name
    """
    try:
        # Truncate text to manage API token limits
        truncated_text = text[:2000]  # Limit text to 2000 characters
        
        # Detailed prompt for consistent categorization
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",  # Using the most capable model
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are an expert screenshot categorization assistant. 
                    Categorize screenshots into these precise categories:
                    1. Work: Professional documents, emails, reports, presentations
                    2. Social Media: Social platform screenshots, posts, chats
                    3. Study: Educational materials, lecture notes, assignments, code, coding
                    4. Personal: Personal communications, memories, recipes
                    5. Finance: Bank statements, receipts, invoices
                    6. Uncategorized: Content that doesn't fit other categories

                    Respond ONLY with the most appropriate category name.
                    Be specific and choose the most precise category.
                    """
                },
                {
                    "role": "user",
                    "content": f"Categorize this screenshot text: {truncated_text}\n\nCategory:"
                }
            ],
            max_tokens=20,
            temperature=0.2,  # Low temperature for consistent results
            top_p=0.9
        )
        
        # Extract and validate category
        category = response.choices[0].message.content.strip()
        
        # Predefined valid categories
        valid_categories = [
            "Work", "Social Media", "Study", 
            "Personal", "Finance", "Uncategorized"
        ]
        
        # Ensure return of a valid category
        return category if category in valid_categories else "Uncategorized"
    
    except Exception as e:
        logging.error(f"Groq Categorization Error: {e}")
        return "Uncategorized"

class ScreenshotHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Check if it's a valid image file
        if event.is_directory or not event.src_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            return
        
        logging.info(f"New screenshot detected: {event.src_path}")
        
        try:
            # Open and extract text from image
            with Image.open(event.src_path) as image:
                # Improved OCR with additional parsing
                text = pytesseract.image_to_string(
                    image, 
                    config='--psm 6'  # Assume a single uniform block of text
                )
            
            # Categorize using Groq API
            category = categorize_screenshot_with_groq(text)
            
            # Create category folder if not exists
            category_path = os.path.join(output_folder, category)
            os.makedirs(category_path, exist_ok=True)
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.basename(event.src_path)
            name, ext = os.path.splitext(filename)
            unique_filename = f"{name}_{timestamp}{ext}"
            
            # Move screenshot to categorized folder
            destination_path = os.path.join(category_path, unique_filename)
            shutil.move(event.src_path, destination_path)
            
            logging.info(f"Moved screenshot to: {destination_path} (Category: {category})")
        
        except Exception as e:
            logging.error(f"Error processing {event.src_path}: {e}")

def main():
    # Validate Groq API key
    if not os.getenv('GROQ_API_KEY'):
        logging.critical("Groq API key not found. Set GROQ_API_KEY environment variable.")
        return
    
    # Create observer
    observer = Observer()
    event_handler = ScreenshotHandler()
    
    # Schedule monitoring
    observer.schedule(event_handler, screenshot_folder, recursive=False)
    observer.start()
    
    logging.info(f"Monitoring {screenshot_folder} for new screenshots...")
    
    try:
        # Keep script running
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
    finally:
        observer.join()

if __name__ == "__main__":
    main()
