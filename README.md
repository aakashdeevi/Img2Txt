# 🖼 Img2Txt - OCR Image to Text Converter

**Img2Txt** is a powerful web application that extracts text from images using Optical Character Recognition (OCR) technology. It supports multiple input methods including direct image uploads, image URLs, and batch processing via Excel files, with built-in grammar correction for extracted text.

<p align="center">
  <img src="https://drive.google.com/uc?export=view&id=1XDTKwdjnfl4Jukxhkjd9JBZz0tJzvo4x" alt="Img2Txt Interface" width="80%"/>
  <br>
  <em>Img2Txt's modern interface with dark mode support</em>
</p>

## 🌐 Live Demo

Experience Img2Txt right now:  
 **[Live Demo on Railway](https://img2txt-production.up.railway.app/)**

---

## ✨ Key Features

###  Multiple Input Methods
- **Local Image Upload**: Drag & drop or select images from your device
- **Image URL**: Extract text from web images with just a URL
- **Excel Batch Processing**: Process multiple images at once via Excel files
- **Base64 Support**: Handle encoded image data directly

###  Advanced OCR Capabilities
- Powered by **OCR.space API** for accurate text extraction
- **Grammar Correction**: Integrated LanguageTool for text refinement
- **Image Optimization**: Automatic resizing and format conversion
- **Bulk Processing**: Handle multiple images simultaneously

###  User-Friendly Interface
-  Dark/Light mode toggle
-  Fully responsive design
-  Real-time progress indicators
-  One-click text copying
-  Intuitive tab-based navigation

###  Output Options
- View extracted text directly in the browser
- Download processed Excel files with all results
- Copy text to clipboard with a single click

---

##  Technical Implementation

###  Core Technologies
- **Backend**: Flask (Python)
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **OCR Engine**: OCR.space API
- **Grammar Checking**: LanguageTool
- **Image Processing**: Pillow (PIL)
- **Data Handling**: Pandas

### 🗂️ Project Structure

```
Img2Txt/
├── app.py               # Flask application (main backend)
├── templates/
│   └── index.html       # Main frontend template
├── static/              # Static assets (CSS/JS)
├── uploads/             # Temporary file storage
├── requirements.txt     # Python dependencies
├── Dockerfile           # Containerization configuration
└── README.md            # Project documentation
```


### 🌐 API Integration
- **OCR.space API**: Handles the actual text extraction from images
- **LanguageTool**: Provides grammar checking for extracted text
- **Rate Limiting**: Built-in error handling for API limits

---

##  Getting Started

### Prerequisites
- Python 3.7+
- pip package manager
- OCR.space API key (free tier available)


###  Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Img2Txt.git
   cd Img2Txt
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment**:
   ```bash
   export API_KEY='your_ocr.space_api_key'
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the app** at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

###  Docker Deployment

1. **Build the Docker image**:
   ```bash
   docker build -t img2txt .
   ```

2. **Run the Docker container**:
   ```bash
   docker run -p 5000:5000 -e API_KEY='your_key' img2txt
   ```

---

###  File Formats

####  Excel Input Format

For batch processing, prepare an Excel file with **at least one column named `Image_URL`**:

```csv
Image_URL,Notes
https://example.com/image1.jpg,Product label
https://example.com/image2.png,Document scan
```

####  Supported Image Formats

- **JPEG / JPG**
- **PNG**
- **GIF**
- **BMP**
- **TIFF**

###  Usage Guide

####  Single Image Processing

1. Select the **"Upload Local Image"** tab  
2. Click to select or **drag & drop** an image  
3. View the **extracted text** in the **Results** tab  

---

####  Batch Processing

1. Prepare an **Excel file** with image URLs (see format above)  
2. Select the **"Excel Sheet"** option  
3. Upload your Excel file  
4. Download the **processed results** with extracted text  

