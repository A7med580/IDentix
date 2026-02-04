import cv2
import numpy as np

def detect_and_align_face(image_path):
    """
    Detects faces in an image and returns the aligned face region.
    Using Haar Cascades for basic detection.
    """
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) == 0:
        return None
    
    # Take the largest face
    (x, y, w, h) = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)[0]
    face_roi = img[y:y+h, x:x+w]
    
    # Resize to standard size for DeepFace
    face_roi = cv2.resize(face_roi, (224, 224))
    
    return face_roi

def normalize_face(face_img):
    """
    Normalizes face image intensity.
    """
    if face_img is None:
        return None
    return face_img.astype('float32') / 255.0
