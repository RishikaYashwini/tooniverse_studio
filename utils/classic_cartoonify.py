import cv2
import numpy as np
from PIL import Image

def resize_for_processing(image, max_dimension=800):
    """
    Resize image if too large to speed up processing.
    Maintains aspect ratio.
    """
    width, height = image.size
    
    if max(width, height) > max_dimension:
        if width > height:
            new_width = max_dimension
            new_height = int((max_dimension / width) * height)
        else:
            new_height = max_dimension
            new_width = int((max_dimension / height) * width)
        
        return image.resize((new_width, new_height), Image.LANCZOS)
    return image

def run_classic_cartoonify(image, edge_threshold=100, bilateral_d=9, num_colors=8):
    """
    Optimized classic cartoon effect with faster processing.
    
    Args:
        image: PIL Image
        edge_threshold: Threshold for edge detection (default: 100)
        bilateral_d: Diameter for bilateral filter (default: 9)
        num_colors: Number of colors for quantization (default: 8)
    
    Returns:
        PIL Image with cartoon effect applied
    """
    # Store original size
    original_size = image.size
    
    # Resize for faster processing
    image_resized = resize_for_processing(image, max_dimension=800)
    
    # Convert PIL to OpenCV format
    img_array = np.array(image_resized)
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    # Step 1: Edge detection (optimized)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(
        gray, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 
        blockSize=9, 
        C=2
    )
    
    # Step 2: Simplified bilateral filtering (single pass instead of two)
    # Reduced from 2 iterations to 1 for speed
    color = cv2.bilateralFilter(img_cv, bilateral_d, 75, 75)
    
    # Step 3: Faster color quantization using downsampling
    # Downsample for k-means to speed up
    small = cv2.resize(color, (0, 0), fx=0.5, fy=0.5)
    data = np.float32(small).reshape((-1, 3))
    
    # K-means with reduced iterations
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(
        data, num_colors, None, criteria, 5, cv2.KMEANS_PP_CENTERS
    )
    
    # Apply quantization to full-size image
    centers = np.uint8(centers)
    quantized_small = centers[labels.flatten()].reshape(small.shape)
    quantized = cv2.resize(quantized_small, (color.shape[1], color.shape[0]))
    
    # Step 4: Combine edges with quantized image
    cartoon = cv2.bitwise_and(quantized, quantized, mask=edges)
    
    # Convert back to PIL and resize to original dimensions
    cartoon_rgb = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
    result = Image.fromarray(cartoon_rgb)
    
    # Resize back to original size if needed
    if image_resized.size != original_size:
        result = result.resize(original_size, Image.LANCZOS)
    
    return result
