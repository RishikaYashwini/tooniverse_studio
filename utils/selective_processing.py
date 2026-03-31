import numpy as np
from PIL import Image
import cv2

def apply_selective_effect(original_image, processed_image, mask):
    """
    Apply processed effect only to masked regions.
    
    Args:
        original_image: PIL Image (original)
        processed_image: PIL Image (cartoonified/styled)
        mask: PIL Image (binary mask)
    
    Returns:
        PIL Image with selective processing
    """
    # Convert to numpy arrays
    original = np.array(original_image)
    processed = np.array(processed_image)
    mask_array = np.array(mask)
    
    # Ensure mask is binary
    if len(mask_array.shape) == 3:
        mask_array = cv2.cvtColor(mask_array, cv2.COLOR_RGB2GRAY)
    
    # Normalize mask to 0-1
    mask_normalized = mask_array.astype(float) / 255.0
    
    # Expand mask to 3 channels
    mask_3d = np.stack([mask_normalized] * 3, axis=2)
    
    # Blend: processed where mask is white, original where mask is black
    result = (processed * mask_3d + original * (1 - mask_3d)).astype(np.uint8)
    
    return Image.fromarray(result)

def apply_background_blur(image, mask, blur_strength=15):
    """
    Blur background while keeping foreground sharp.
    
    Args:
        image: PIL Image
        mask: PIL Image (binary mask - white=keep sharp)
        blur_strength: Blur intensity
    
    Returns:
        PIL Image with blurred background
    """
    img_array = np.array(image)
    mask_array = np.array(mask)
    
    # Ensure mask is binary
    if len(mask_array.shape) == 3:
        mask_array = cv2.cvtColor(mask_array, cv2.COLOR_RGB2GRAY)
    
    # Blur the entire image
    blurred = cv2.GaussianBlur(img_array, (blur_strength, blur_strength), 0)
    
    # Normalize mask
    mask_normalized = mask_array.astype(float) / 255.0
    mask_3d = np.stack([mask_normalized] * 3, axis=2)
    
    # Keep original where mask is white, blurred where mask is black
    result = (img_array * mask_3d + blurred * (1 - mask_3d)).astype(np.uint8)
    
    return Image.fromarray(result)
