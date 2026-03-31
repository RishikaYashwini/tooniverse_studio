import cv2
import numpy as np
from PIL import Image
import mediapipe as mp

class CartoonAnimator:
    """
    Create visible animations from cartoonified images.
    """
    
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1,
            min_detection_confidence=0.5
        )
    
    def create_bounce_animation(self, image, num_frames=20):
        """
        Create VISIBLE bouncing animation with scaling.
        """
        frames = []
        img_array = np.array(image)
        h, w = img_array.shape[:2]
        
        # Create canvas larger than image for bounce room
        canvas_h = h + 100
        canvas_w = w + 40
        
        for i in range(num_frames):
            # Sine wave for smooth bounce
            progress = i / num_frames
            bounce = int(50 * abs(np.sin(progress * 2 * np.pi)))
            
            # Scale effect during bounce
            scale = 1.0 + 0.1 * abs(np.sin(progress * 2 * np.pi))
            
            # Create white canvas
            canvas = np.ones((canvas_h, canvas_w, 3), dtype=np.uint8) * 255
            
            # Resize image with scale
            scaled_h = int(h * scale)
            scaled_w = int(w * scale)
            scaled_img = cv2.resize(img_array, (scaled_w, scaled_h))
            
            # Calculate position (centered horizontally, bouncing vertically)
            y_offset = canvas_h - scaled_h - bounce - 20
            x_offset = (canvas_w - scaled_w) // 2
            
            # Ensure offsets are valid
            y_offset = max(0, min(y_offset, canvas_h - scaled_h))
            x_offset = max(0, min(x_offset, canvas_w - scaled_w))
            
            # Place image on canvas
            try:
                canvas[y_offset:y_offset+scaled_h, x_offset:x_offset+scaled_w] = scaled_img
            except:
                canvas[20:20+h, 20:20+w] = img_array
            
            frames.append(Image.fromarray(canvas))
        
        return frames
    
    def create_blink_animation(self, image, num_frames=20):
        """
        Create VISIBLE eye blink animation with face detection.
        """
        frames = []
        img_array = np.array(image)
        
        # Detect face
        results = self.face_detection.process(img_array)
        
        if results.detections:
            h, w = img_array.shape[:2]
            detection = results.detections[0]
            bbox = detection.location_data.relative_bounding_box
            
            # Eye region (upper part of face)
            face_x = int(bbox.xmin * w)
            face_y = int(bbox.ymin * h)
            face_w = int(bbox.width * w)
            face_h = int(bbox.height * h)
            
            # Eye region is approximately top 40% of face
            eye_y1 = max(0, face_y + int(face_h * 0.2))
            eye_y2 = min(h, face_y + int(face_h * 0.5))
            eye_x1 = max(0, face_x)
            eye_x2 = min(w, face_x + face_w)
            
            for i in range(num_frames):
                frame = img_array.copy()
                
                # Blink in middle frames (frames 8-12 for closing/opening)
                if 7 <= i <= 13:
                    # Calculate blink intensity (0=no blink, 1=full blink)
                    if i <= 10:
                        intensity = (i - 7) / 3.0  # Closing
                    else:
                        intensity = (13 - i) / 3.0  # Opening
                    
                    # Darken eye region
                    eye_region = frame[eye_y1:eye_y2, eye_x1:eye_x2].copy()
                    darkened = (eye_region * (1 - 0.7 * intensity)).astype(np.uint8)
                    frame[eye_y1:eye_y2, eye_x1:eye_x2] = darkened
                    
                    # Add horizontal line for closed eye effect
                    if intensity > 0.5:
                        eye_line_y = (eye_y1 + eye_y2) // 2
                        cv2.line(frame, (eye_x1, eye_line_y), 
                                (eye_x2, eye_line_y), (0, 0, 0), 2)
                
                frames.append(Image.fromarray(frame))
        else:
            # No face detected, create simple brightness blink
            for i in range(num_frames):
                frame = img_array.copy()
                if 8 <= i <= 12:
                    brightness = 1.0 - 0.3 * abs((i - 10) / 2.0)
                    frame = (frame * brightness).astype(np.uint8)
                frames.append(Image.fromarray(frame))
        
        return frames
    
    def create_shake_animation(self, image, num_frames=15):
        """
        Create head shake animation.
        """
        frames = []
        img_array = np.array(image)
        h, w = img_array.shape[:2]
        
        # Create canvas with padding
        canvas_w = w + 60
        canvas_h = h + 20
        
        for i in range(num_frames):
            # Horizontal shake (sine wave)
            shake = int(30 * np.sin(i / num_frames * 4 * np.pi))
            
            # Create white canvas
            canvas = np.ones((canvas_h, canvas_w, 3), dtype=np.uint8) * 255
            
            # Calculate position
            x_offset = 30 + shake
            y_offset = 10
            
            # Place image
            canvas[y_offset:y_offset+h, x_offset:x_offset+w] = img_array
            
            frames.append(Image.fromarray(canvas))
        
        return frames

def run_animation(image, animation_type="bounce", num_frames=20):
    """
    Create animated version with VISIBLE effects.
    """
    animator = CartoonAnimator()
    
    if animation_type == "bounce":
        return animator.create_bounce_animation(image, num_frames)
    elif animation_type == "blink":
        return animator.create_blink_animation(image, num_frames)
    elif animation_type == "shake":
        return animator.create_shake_animation(image, num_frames)
    
    return [image]

def save_animation_gif(frames, duration=100):
    """
    Helper to ensure GIF is properly animated.
    
    Args:
        frames: List of PIL Images
        duration: Milliseconds per frame (100 = 0.1 seconds)
    
    Returns:
        Bytes of animated GIF
    """
    if len(frames) < 2:
        frames = frames * 2  # Duplicate if only one frame
    
    gif_buffer = io.BytesIO()
    frames[0].save(
        gif_buffer,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        format='GIF',
        optimize=False,  # Important: Don't optimize
        disposal=2  # Clear frame before next
    )
    gif_buffer.seek(0)
    return gif_buffer.getvalue()