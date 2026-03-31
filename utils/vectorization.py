import cv2
import numpy as np
from PIL import Image
import svgwrite

class VectorConverter:
    """
    Convert cartoonified images to vector SVG format.
    Uses contour detection for vectorization.
    """
    
    def __init__(self):
        pass
    
    def image_to_svg(self, image, output_path, simplify_level=2):
        """
        Convert image to SVG using contour tracing.
        
        Args:
            image: PIL Image
            output_path: Path to save SVG file
            simplify_level: Contour simplification (1-5, higher = simpler)
        
        Returns:
            Path to saved SVG file
        """
        # Convert PIL to OpenCV
        img_array = np.array(image)
        img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # Resize for faster processing
        h, w = img_cv.shape[:2]
        max_dim = 512
        if max(h, w) > max_dim:
            scale = max_dim / max(h, w)
            img_cv = cv2.resize(img_cv, None, fx=scale, fy=scale)
            h, w = img_cv.shape[:2]
        
        # Create SVG
        dwg = svgwrite.Drawing(output_path, size=(w, h), profile='tiny')
        
        # Add white background
        dwg.add(dwg.rect(insert=(0, 0), size=(w, h), fill='white'))
        
        # Process each color layer
        colors = self._extract_dominant_colors(img_cv, num_colors=8)
        
        for color in colors:
            # Create mask for this color
            mask = self._create_color_mask(img_cv, color, tolerance=30)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Convert color to hex
            color_hex = '#{:02x}{:02x}{:02x}'.format(int(color[2]), int(color[1]), int(color[0]))
            
            # Draw contours as SVG paths
            for contour in contours:
                if len(contour) > 10:  # Skip tiny contours
                    # Simplify contour
                    epsilon = simplify_level * 0.001 * cv2.arcLength(contour, True)
                    simplified = cv2.approxPolyDP(contour, epsilon, True)
                    
                    # Convert to SVG path
                    if len(simplified) > 2:
                        points = [(int(pt[0][0]), int(pt[0][1])) for pt in simplified]
                        dwg.add(dwg.polygon(points=points, fill=color_hex, stroke='none'))
        
        # Save SVG
        dwg.save()
        return output_path
    
    def _extract_dominant_colors(self, img, num_colors=8):
        """
        Extract dominant colors using k-means clustering.
        """
        pixels = img.reshape(-1, 3).astype(np.float32)
        
        # K-means clustering
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, labels, centers = cv2.kmeans(
            pixels, num_colors, None, criteria, 5, cv2.KMEANS_PP_CENTERS
        )
        
        # Sort by frequency
        unique, counts = np.unique(labels, return_counts=True)
        sorted_indices = np.argsort(-counts)
        
        return centers[sorted_indices]
    
    def _create_color_mask(self, img, target_color, tolerance=30):
        """
        Create binary mask for pixels matching target color.
        Fixed: Ensure lower and upper bounds have same data type.
        """
        # Ensure target_color is uint8 (integer type)
        target_color = np.array(target_color, dtype=np.uint8)
        
        # Create bounds with same data type (uint8)
        lower = np.array([
            max(0, int(c) - tolerance) for c in target_color
        ], dtype=np.uint8)
        
        upper = np.array([
            min(255, int(c) + tolerance) for c in target_color
        ], dtype=np.uint8)
        
        # Ensure image is also uint8
        img = img.astype(np.uint8)
        
        mask = cv2.inRange(img, lower, upper)
        
        # Clean up mask
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        return mask

def convert_to_svg(image, output_path, simplify_level=2):
    """
    Convert image to SVG vector format.
    
    Args:
        image: PIL Image
        output_path: Path to save SVG
        simplify_level: Simplification level (1-5)
    
    Returns:
        Path to saved SVG file
    """
    converter = VectorConverter()
    return converter.image_to_svg(image, output_path, simplify_level)
