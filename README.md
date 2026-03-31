# 🎨 Tooniverse Studio

**An AI-Powered Image Cartoonification Platform**

Transform your photos into stunning cartoons with multiple artistic styles, intelligent segmentation, animation effects, and vector export capabilities.

---

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
- [Module Documentation](#module-documentation)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)
- [Contributors](#contributors)

---

## ✨ Features

### 🎨 Classic Cartoonify Engine
- **Edge Detection**: Adaptive thresholding for clean cartoon outlines
- **Bilateral Filtering**: Smooth color regions while preserving edges
- **Color Quantization**: K-means clustering for simplified color palettes
- **Preset Modes**: Bold, Soft, Minimal, and Detailed presets
- **Manual Controls**: Fine-tune edge intensity, smoothness, and color count

### 🤖 AI Style Studio
Three distinct artistic styles powered by advanced image processing:

1. **Cartoon Style**: Bold edges, flat colors (Western animation style)
   - Thick black contours
   - Simplified color palette
   - High saturation

2. **Anime Style**: Vibrant colors, thin lines (Japanese animation style)
   - Delicate edge detection
   - Rich color variety
   - Enhanced brightness and saturation

3. **Comic Style**: High contrast, dramatic shadows (Comic book style)
   - Medium-weight edges
   - High contrast enhancement
   - Halftone dot effects

### 🎯 Content-Aware Segmentation
- **Face Detection**: MediaPipe-powered face localization
- **Foreground Separation**: GrabCut algorithm for automatic subject extraction
- **Selective Processing**: Apply effects only to masked regions
- **Background Blur**: Focus on subjects with intelligent blurring

### 🎬 Living Cartoon Animation
- **Bounce Effect**: Vertical movement with dynamic scaling
- **Shake Effect**: Horizontal oscillation for expressive motion
- **GIF Export**: High-quality animated GIF generation
- **Customizable Frames**: Adjust animation smoothness

### 🎨 Vector Export (SVG)
- **Contour-Based Vectorization**: Convert raster to scalable vectors
- **Color Layer Separation**: Intelligent color segmentation
- **Simplification Control**: Adjust detail level for optimal file size
- **Professional Output**: Edit in vector graphics software

---

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.8+**: Primary programming language
- **Streamlit**: Interactive web application framework
- **OpenCV**: Computer vision and image processing
- **NumPy**: Numerical computing and array operations

### AI/ML Libraries
- **MediaPipe**: Face detection and mesh generation
- **PyTorch**: Deep learning framework (future extensions)
- **scikit-image**: Advanced image processing algorithms

### Additional Libraries
- **Pillow (PIL)**: Image manipulation
- **svgwrite**: SVG generation
- **imageio**: GIF creation and video I/O
- **scipy**: Scientific computing utilities

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Step-by-Step Setup

1. **Clone or Download the Project**
cd tooniverse-studio

2. **Create Virtual Environment**
Windows
python -m venv venv
venv\Scripts\activate

macOS/Linux
python3 -m venv venv
source venv/bin/activate

3. **Install Dependencies**
pip install -r requirements.txt

4. **Run the Application**
streamlit run app.py

5. **Open in Browser**
The app will automatically open at `http://localhost:8501`

---

## 📖 Usage Guide

### Quick Start

1. **Upload Image**
   - Click "Browse files" in the sidebar
   - Select JPG, PNG, or JPEG image
   - Wait for upload confirmation

2. **Choose Style**
   - **Classic Studio**: Use presets or manual controls
   - **AI Style Studio**: Select Cartoon, Anime, or Comic

3. **Apply Effect**
   - Click the apply button for your chosen style
   - Preview result in real-time
   - Adjust parameters and reapply if needed

4. **Advanced Features** (Optional)
   - Create segmentation mask for selective effects
   - Generate animations (Bounce/Shake)
   - Export as PNG, GIF, or SVG

### Tips for Best Results

✅ **Image Quality**: Use high-resolution images (min 800x800px)
✅ **Face Detection**: Ensure faces are well-lit and clearly visible
✅ **Presets**: Start with presets, then fine-tune manually
✅ **Segmentation**: Works best with clear subject-background separation
✅ **Animation**: Use processed images for better animation effects

---

## 📁 Project Structure
tooniverse-studio/
├── .streamlit/
│ └── config.toml # Streamlit theme configuration
├── app.py # Main application entry point
├── utils/
│ ├── init.py # Package initializer
│ ├── classic_cartoonify.py # Classic cartoon algorithm
│ ├── ai_style_transfer.py # AI-powered style effects
│ ├── segmentation.py # Content-aware segmentation
│ ├── selective_processing.py # Mask-based processing
│ ├── animation.py # GIF animation generation
│ ├── vectorization.py # SVG vector conversion
│ └── presets.py # Preset configurations
├── models/ # Pre-trained AI models (optional)
├── assets/ # Sample images and resources
├── requirements.txt # Python dependencies
└── README.md # This file

---

## 🔧 Module Documentation

### `classic_cartoonify.py`
**Core Functionality**: Traditional cartoon effect using edge detection and color quantization

**Key Functions**:
- `run_classic_cartoonify(image, edge_threshold, bilateral_d, num_colors)`
  - **Parameters**: 
    - `edge_threshold`: Edge detection sensitivity (1-200)
    - `bilateral_d`: Smoothing kernel diameter (3-15)
    - `num_colors`: Color palette size (4-16)
  - **Returns**: PIL Image with cartoon effect

**Algorithm Steps**:
1. Edge Detection: Adaptive thresholding on grayscale image
2. Bilateral Filtering: Preserve edges while smoothing colors
3. K-means Clustering: Quantize colors to simplified palette
4. Edge Overlay: Combine edges with quantized image

### `ai_style_transfer.py`
**Core Functionality**: Artistic style transformation with distinct visual characteristics

**Key Classes**:
- `StyleTransfer`: Main style processing engine

**Methods**:
- `apply_cartoon_style()`: Bold edges, flat colors
- `apply_anime_style()`: Vibrant colors, thin lines
- `apply_comic_style()`: High contrast, halftone effects

### `segmentation.py`
**Core Functionality**: Intelligent region detection and masking

**Key Classes**:
- `ImageSegmenter`: Face and foreground detection

**Methods**:
- `detect_faces()`: MediaPipe face detection
- `create_face_mask()`: Binary mask for face regions
- `grabcut_segmentation()`: Automatic foreground extraction

### `animation.py`
**Core Functionality**: Frame generation for animated GIFs

**Key Classes**:
- `CartoonAnimator`: Animation effect generator

**Methods**:
- `create_bounce_animation()`: Vertical bouncing with scaling
- `create_shake_animation()`: Horizontal shake effect

### `vectorization.py`
**Core Functionality**: Raster to vector conversion using contour tracing

**Key Classes**:
- `VectorConverter`: SVG generation engine

**Methods**:
- `image_to_svg()`: Convert image to scalable vector graphics
- `_extract_dominant_colors()`: K-means color extraction
- `_create_color_mask()`: Color-based region segmentation

---

## 📸 Screenshots

### Main Interface
![Main Interface](assets/screenshot_main.png)

### Classic Cartoon Effect
![Classic Effect](assets/screenshot_classic.png)

### AI Style Comparison
![AI Styles](assets/screenshot_ai_styles.png)

### Animation Preview
![Animation](assets/screenshot_animation.gif)

---

## 🚀 Future Enhancements

### Short-term Goals
- [ ] Batch processing for multiple images
- [ ] More animation types (Wave, Spin, Pulse)
- [ ] Custom color palette selection
- [ ] Before/After slider comparison

### Long-term Goals
- [ ] Deep learning-based style transfer (GAN models)
- [ ] Video cartoonification support
- [ ] Real-time webcam processing
- [ ] Mobile app version
- [ ] Cloud deployment with user accounts

---

## 📊 Performance Optimization

**Processing Times** (on standard laptop):
- Classic Cartoonify: 1-3 seconds
- AI Style Transfer: 2-4 seconds
- Segmentation: 1-2 seconds
- Animation (20 frames): 3-5 seconds
- SVG Vectorization: 4-6 seconds

**Optimizations Applied**:
- Image downscaling before processing
- Reduced k-means iterations
- Single-pass bilateral filtering
- Efficient contour simplification

---

## 🎓 Academic Context

**Course**: Computer Graphics and Image Processing
**Project Type**: Mini Project
**Semester**: 3rd Year
**Institution**: Dr. AIT

**Learning Outcomes**:
1. Understanding of image processing algorithms
2. Implementation of edge detection techniques
3. Color space manipulation and quantization
4. Computer vision algorithms (face detection, segmentation)
5. Real-time application development
6. User interface design principles

---

## 🤝 Contributors

**Developer**: Rishika Yashwini
**Institution**: Dr. AIT
**Year**: 3rd Year
**Contact**: [Your Email]

---

## 📄 License

This project is developed for academic purposes as part of the Computer Graphics and Image Processing course.

---

## 🙏 Acknowledgments

- **OpenCV Community**: For comprehensive computer vision tools
- **Streamlit Team**: For the intuitive web framework
- **MediaPipe**: For advanced ML solutions
- **Course Instructors**: For guidance and support

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on the project repository
- Contact the developer via email
- Refer to the documentation

---

**Made with ❤️ using Python, OpenCV, and Streamlit**

---

*Last Updated: November 2025*
