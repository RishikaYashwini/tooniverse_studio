import cv2
import numpy as np
from PIL import Image
import mediapipe as mp
# Direct top-level solution imports
import mediapipe.solutions.face_detection as mp_face_detection
import mediapipe.solutions.selfie_segmentation as mp_selfie_segmentation

class ImageSegmenter:
    """
    Content-aware segmentation for selective processing.
    Uses MediaPipe for face detection and simplified segmentation.
    """
    
    def __init__(self):
        # Initialize MediaPipe Face Detection
        self.mp_face_detection = mp_face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1,
            min_detection_confidence=0.5
        )
    
    def detect_faces(self, image):
        """
        Detect faces in the image.
        
        Args:
            image: PIL Image
        
        Returns:
            List of face bounding boxes [(x, y, w, h), ...]
        """
        # Convert to RGB numpy array
        img_array = np.array(image)
        
        # Process with MediaPipe
        results = self.face_detection.process(img_array)
        
        faces = []
        if results.detections:
            h, w = img_array.shape[:2]
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)
                faces.append((x, y, width, height))
        
        return faces
    
    def create_face_mask(self, image):
        """
        Create a binary mask highlighting face regions.
        
        Args:
            image: PIL Image
        
        Returns:
            PIL Image (binary mask)
        """
        img_array = np.array(image)
        h, w = img_array.shape[:2]
        
        # Create empty mask
        mask = np.zeros((h, w), dtype=np.uint8)
        
        # Detect faces
        faces = self.detect_faces(image)
        
        if len(faces) == 0:
            # If no faces detected, return empty mask
            return Image.fromarray(mask)
        
        # Fill face regions
        for (x, y, width, height) in faces:
            # Add padding around face
            padding = 20
            x1 = max(0, x - padding)
            y1 = max(0, y - padding)
            x2 = min(w, x + width + padding)
            y2 = min(h, y + height + padding)
            
            # Create smooth circular mask
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            radius = max(width, height) // 2 + padding
            
            cv2.circle(mask, (center_x, center_y), radius, 255, -1)
        
        return Image.fromarray(mask)
    
    def grabcut_segmentation(self, image, iterations=3):
        """
        Memory-efficient foreground/background segmentation.
        
        Args:
            image: PIL Image
            iterations: Number of GrabCut iterations (reduced for memory)
        
        Returns:
            PIL Image (binary mask)
        """
        img_array = np.array(image)
        
        # CRITICAL FIX: Resize image if too large to prevent memory error
        h, w = img_array.shape[:2]
        max_dimension = 512  # Limit size for GrabCut
        
        if max(h, w) > max_dimension:
            scale = max_dimension / max(h, w)
            new_w = int(w * scale)
            new_h = int(h * scale)
            img_resized = cv2.resize(img_array, (new_w, new_h))
        else:
            img_resized = img_array.copy()
            new_w, new_h = w, h
        
        # Ensure image is in correct format (3 channels, uint8)
        if len(img_resized.shape) == 2:
            img_resized = cv2.cvtColor(img_resized, cv2.COLOR_GRAY2BGR)
        elif img_resized.shape[2] == 4:
            img_resized = cv2.cvtColor(img_resized, cv2.COLOR_RGBA2BGR)
        
        img_resized = img_resized.astype(np.uint8)
        
        # Create rectangle for GrabCut (with margin)
        margin = int(min(new_h, new_w) * 0.05)
        rect = (margin, margin, new_w - 2*margin, new_h - 2*margin)
        
        # Validate rectangle
        if rect[2] <= 0 or rect[3] <= 0:
            # Return full mask if rectangle is invalid
            return Image.fromarray(np.ones((h, w), dtype=np.uint8) * 255)
        
        try:
            # Initialize mask and models with correct sizes
            mask = np.zeros(img_resized.shape[:2], dtype=np.uint8)
            bgd_model = np.zeros((1, 65), dtype=np.float64)
            fgd_model = np.zeros((1, 65), dtype=np.float64)
            
            # Apply GrabCut with reduced iterations
            cv2.grabCut(
                img_resized, mask, rect, 
                bgd_model, fgd_model, 
                iterations, 
                cv2.GC_INIT_WITH_RECT
            )
            
            # Create binary mask
            mask2 = np.where((mask == 2) | (mask == 0), 0, 255).astype('uint8')
            
            # Resize mask back to original size
            if max(h, w) > max_dimension:
                mask2 = cv2.resize(mask2, (w, h), interpolation=cv2.INTER_NEAREST)
            
            return Image.fromarray(mask2)
            
        except Exception as e:
            print(f"GrabCut error: {str(e)}")
            # Return full white mask on error
            return Image.fromarray(np.ones((h, w), dtype=np.uint8) * 255)

def run_segmentation(image, mode="face"):
    """
    Apply segmentation to image.
    
    Args:
        image: PIL Image
        mode: "face" or "foreground"
    
    Returns:
        PIL Image (binary mask)
    """
    segmenter = ImageSegmenter()
    
    if mode == "face":
        return segmenter.create_face_mask(image)
    elif mode == "foreground":
        return segmenter.grabcut_segmentation(image)
    
    return None
