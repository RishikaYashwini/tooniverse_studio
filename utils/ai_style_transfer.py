import cv2
import numpy as np
from PIL import Image

class StyleTransfer:
    """
    Multiple distinct cartoon styles: Cartoon, Anime, Comic.
    Each style has unique visual characteristics.
    """
    
    def __init__(self):
        pass
    
    def apply_cartoon_style(self, img_cv, strength):
        """
        Classic Western cartoon style: Bold edges, simplified colors.
        """
        # Strong bilateral filtering for flat colors
        smooth = cv2.bilateralFilter(img_cv, 9, 90, 90)
        
        # Color quantization - fewer colors for cartoon look
        num_colors = max(4, int(8 - strength * 4))
        data = np.float32(smooth).reshape((-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, labels, centers = cv2.kmeans(data, num_colors, None, criteria, 5, cv2.KMEANS_PP_CENTERS)
        centers = np.uint8(centers)
        quantized = centers[labels.flatten()].reshape(smooth.shape)
        
        # THICK black edges for classic cartoon look
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 7)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY, 9, 2)
        
        # Make edges thicker
        kernel = np.ones((2, 2), np.uint8)
        edges = cv2.erode(edges, kernel, iterations=1)
        
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        result = cv2.bitwise_and(quantized, edges_colored)
        
        # Boost saturation
        hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.3, 0, 255)
        result = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
        return result
    
    def apply_anime_style(self, img_cv, strength):
        """
        Japanese anime style: Soft colors, thin lines, high saturation.
        """
        # Gentle smoothing - anime has more detail than cartoons
        smooth = cv2.bilateralFilter(img_cv, 7, 50, 50)
        
        # More colors than cartoon (anime has richer palette)
        num_colors = max(8, int(12 - strength * 3))
        data = np.float32(smooth).reshape((-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, labels, centers = cv2.kmeans(data, num_colors, None, criteria, 5, cv2.KMEANS_PP_CENTERS)
        centers = np.uint8(centers)
        quantized = centers[labels.flatten()].reshape(smooth.shape)
        
        # THIN, delicate edges for anime style
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        edges = cv2.Canny(gray, 50, 150)
        edges = cv2.dilate(edges, None, iterations=1)
        edges = 255 - edges  # Invert
        
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        result = cv2.bitwise_and(quantized, edges_colored)
        
        # HIGH saturation and slight brightness boost (anime is vibrant)
        hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.5, 0, 255)  # More saturation
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.1, 0, 255)  # Slight brightness
        result = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
        return result
    
    def apply_comic_style(self, img_cv, strength):
        """
        Comic book style: High contrast, halftone dots, dramatic shadows.
        """
        # Moderate smoothing
        smooth = cv2.bilateralFilter(img_cv, 9, 75, 75)
        
        # Medium color count
        num_colors = max(6, int(10 - strength * 3))
        data = np.float32(smooth).reshape((-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, labels, centers = cv2.kmeans(data, num_colors, None, criteria, 5, cv2.KMEANS_PP_CENTERS)
        centers = np.uint8(centers)
        quantized = centers[labels.flatten()].reshape(smooth.shape)
        
        # Medium-thick edges
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 9, 2)
        
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        result = cv2.bitwise_and(quantized, edges_colored)
        
        # HIGH CONTRAST for comic book drama
        result = cv2.convertScaleAbs(result, alpha=1.3, beta=10)
        
        # Add halftone pattern effect
        result = self._add_halftone_effect(result, strength)
        
        return result
    
    def _add_halftone_effect(self, img, strength):
        """
        Add subtle halftone dots for comic book effect.
        """
        if strength < 0.5:
            return img
        
        h, w = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Create dot pattern
        dot_size = 3
        for y in range(0, h, dot_size * 2):
            for x in range(0, w, dot_size * 2):
                if gray[min(y, h-1), min(x, w-1)] < 100:
                    cv2.circle(img, (x, y), 1, (0, 0, 0), -1)
        
        return img
    
    def process(self, image, style_type, style_strength):
        """
        Apply selected style to image.
        """
        original_size = image.size
        
        # Convert to OpenCV
        img_array = np.array(image)
        img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # Resize for processing
        max_dim = 512
        h, w = img_cv.shape[:2]
        if max(h, w) > max_dim:
            scale = max_dim / max(h, w)
            img_cv = cv2.resize(img_cv, None, fx=scale, fy=scale)
        
        # Apply the selected style
        if style_type == "cartoon":
            result = self.apply_cartoon_style(img_cv, style_strength)
        elif style_type == "anime":
            result = self.apply_anime_style(img_cv, style_strength)
        elif style_type == "comic":
            result = self.apply_comic_style(img_cv, style_strength)
        else:
            result = img_cv
        
        # Resize back
        if max(h, w) > max_dim:
            result = cv2.resize(result, (w, h))
        
        # Convert back to PIL
        result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        return Image.fromarray(result_rgb)

def run_ai_style_transfer(image, style_type="cartoon", style_strength=0.8):
    """
    Apply distinct AI style transfer.
    
    Args:
        image: PIL Image
        style_type: "cartoon", "anime", or "comic"
        style_strength: 0.0 to 1.0
    
    Returns:
        Styled PIL Image
    """
    style_transfer = StyleTransfer()
    return style_transfer.process(image, style_type.lower(), style_strength)
