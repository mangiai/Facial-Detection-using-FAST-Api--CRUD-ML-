from PIL import Image
import cv2
import numpy as np

def detect_faces(image: Image.Image):
    # Sample function body - replace with your actual face detection logic
    # Example: using OpenCV for face detection
    image_cv = np.array(image)  # Convert PIL image to cv2 image format
    gray = cv2.cvtColor(image_cv, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    
    # Just return the count of faces detected for simplicity
    return len(faces)


def crop_face(image_path):
    # Load the image from disk
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Load the pre-trained Haar Cascade model for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        return None  # No faces detected

    # Crop the first detected face
    for (x, y, w, h) in faces:
        face = image[y:y+h, x:x+w]
        cropped_image = Image.fromarray(cv2.cvtColor(face, cv2.COLOR_BGR2RGB))
        return cropped_image

    return None


def detect_and_crop_face(image: Image.Image):
    # Convert PIL image to an OpenCV image
    open_cv_image = np.array(image)
    # Convert RGB to BGR
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    # Load the pre-trained Haar Cascade model for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))

    if faces is not None and len(faces) > 0:
        # Assuming the first detected face is what we want
        (x, y, w, h) = faces[0]
        face = open_cv_image[y:y+h, x:x+w]
        # Convert back to RGB
        pil_image = Image.fromarray(face[:, :, ::-1])
        return pil_image

    # If no faces are detected, return None or the original image
    return None
