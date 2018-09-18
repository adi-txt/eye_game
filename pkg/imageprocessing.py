from PIL import Image
import face_recognition as fr
import numpy as np
import cv2

def pil_to_cv(img_array):
    """
    PIL image object to an OpenCV image object
    """
    return cv2.cvtColor(np.asarray(img_array), cv2.COLOR_RGB2BGR)

def cv2_to_pil(img_array):
    """
    OpenCV image object to a PIL image
    """
    return Image.fromarray(cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB))

def cv2_to_face_recognition(img_array):
    """
    OpenCV image to face_recognition image
    """
    return cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

def pil_to_face_recognition(img_array):
    """
    PIL image to face_recognition image
    """
    return np.array(img_array)

def face_recognition_to_pil(img_array):
    """
    face_recognition image to PIL image
    """
    return Image.fromarray(np.uint8(img_array))
