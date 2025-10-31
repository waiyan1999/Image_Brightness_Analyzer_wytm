# Image_Brightness_Analyzer_wytm
Image_Brightness_Analyzer

# 🔍 Image Brightness Analyzer

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![OpenCV](https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=OpenCV&logoColor=white)
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![MySQL](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white)

*A professional FastAPI application for advanced image brightness analysis*

</div>

## 📋 Table of Contents
- [Overview](#-overview)
- [Quick Start](#-quick-start)
- [Installation Guide](#-installation-guide)
- [API Documentation](#-api-documentation)
- [Features](#-features)
- [Support](#-support)

## 🚀 Overview

The **Image Brightness Analyzer** is a sophisticated FastAPI application that provides comprehensive image analysis capabilities. It detects brightness patterns, identifies extreme points, and generates detailed visual reports with marked coordinates.

## ⚡ Quick Start

### Prerequisites
- Python 3.8 or higher
- MySQL (Optional, for database features)

### Installation Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/waiyan1999/Image_Brightness_Analyzer_wytm.git
   cd Image_Brightness_Analyzer_wytm
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🔧 Installation Guide

### Step-by-Step Setup

#### 1. Environment Configuration
Create a `.env` file in the project root:

```env
# Database Configuration
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=image_analysis

# Application Settings
APP_HOST=0.0.0.0
APP_PORT=8000
```

#### 2. Database Setup (Optional)
Initialize the database by running:
```bash
python database.py
```

#### 3. Start the Server
Choose one of the following methods:

**Method 1: Using FastAPI Dev Server**
```bash
fastapi dev main.py
```

**Method 2: Using Uvicorn Directly**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 4. Access the Application
Once the server is running, you can access:

- 🌐 **Application Server**: http://127.0.0.1:8000
- 📚 **Interactive API Docs**: http://127.0.0.1:8000/docs
- 📖 **Alternative Documentation**: http://127.0.0.1:8000/redoc

## 📊 API Documentation

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/analyze/` | Upload and analyze image brightness |
| `GET` | `/download/{filename}` | Download processed images |
| `GET` | `/results` | View analysis history |


### Example Usage

**1. Analyze an Image:**
```bash
curl -X POST "http://localhost:8000/analyze/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_image.jpg"
```

**2. Sample Response:**
```json
{
  "average_brightness": 134.2,
  "brightest_point": [123, 44],
  "darkest_point": [22, 199],
  "brightest_value": 255,
  "darkest_value": 0,
  "processed_image_url": "http://localhost:8000/results/output_1730123456.png"
}
```

## 🌟 Features

### 🔍 Advanced Analysis
- **Average Brightness Calculation**
- **Extreme Point Detection** (Brightest & Darkest pixels)
- **Coordinate Mapping** with visual markers
- **Real-time Image Processing**

### 💾 Data Management
- **MySQL Integration** for result storage
- **Analysis History** tracking
- **File Download** capabilities
- **Automated Backup** systems

### 🔧 Technical Excellence
- **RESTful API Design**
- **Comprehensive Error Handling**
- **Input Validation**
- **Performance Optimized**

## 🛠 Technical Stack

| Component | Technology |
|-----------|------------|
| **Backend Framework** | FastAPI |
| **Image Processing** | OpenCV, NumPy |
| **Database** | MySQL |
| **API Documentation** | Swagger/OpenAPI |
| **Environment Management** | python-dotenv |

## 🐛 Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **Database Connection Failed** | Check MySQL service and .env credentials |
| **Import Errors** | Verify virtual environment activation |
| **Port 8000 Busy** | Use `sudo lsof -t -i tcp:8000 \| xargs kill -9` |
| **Image Processing Failed** | Verify file format (JPG/PNG only) |

### Verification Steps
1. ✅ Virtual environment activated
2. ✅ All dependencies installed
3. ✅ Database running (if using MySQL)
4. ✅ .env file properly configured
5. ✅ Sufficient disk space in results directory

## 📞 Support

### Developer Information
- **Developer**: Wai Yan Thae Maung
- **Contact**: 09780351988
- **Email**: waiyan1661999@gmail.com
- **GitHub**: https://github.com/waiyan1999

### Getting Help
- 📚 Check the interactive documentation at `/docs`
- 🐛 Report issues on GitHub
- 📧 Contact developer for direct support

---

<div align="center">

### **Happy Coding!** 🎉

*Built with ❤️ using FastAPI and OpenCV*

</div>

---

**Version**: 2.0.0  
**Last Updated**: December 2024  
