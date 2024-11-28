# ScreenSort 📸🗂️

## Overview
ScreenSort is an intelligent screenshot organization tool that automatically categorizes and sorts your screenshots using advanced text recognition and machine learning techniques.

## Features
- Automatic screenshot categorization
- Intelligent text extraction
- Customizable folder organization
- Real-time monitoring of screenshot directory
- Supports multiple image formats

## Installation

### Prerequisites
- Python 3.8+
- Tesseract OCR
- Required Python libraries:
  ```
  pip install pytesseract pillow opencv-python-headless watchdog
  ```

### Setup
1. Clone the repository
2. Install dependencies
3. Configure screenshot directories in `screenshot_organizer.py`
4. Run the script

## Usage
- Place screenshots in designated folder
- ScreenSort automatically sorts them into categories
- Customizable categorization rules

## Supported Categories
- Work
- Code
- Finance
- Personal
- Uncategorized

## Customization
Modify `categories` dictionary to personalize sorting rules.

## Contributing
Contributions welcome! Submit pull requests or open issues.
