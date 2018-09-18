from .functions import get_eye_direction, image_pre_processing
from .direction import get_direction, get_result
from .imageprocessing import (
    pil_to_cv,
    cv2_to_pil,
    pil_to_face_recognition,
    face_recognition_to_pil,
    cv2_to_face_recognition,
)

import cv2

def get_eyeball_direction(image_path):
    cv_img_array = cv2.imread(image_path)

    try:
        result = image_pre_processing(cv_img_array)

        if result is not None:
            result = get_eye_direction(
                result["cv_img_array"],
                result["eye_locations"]
            )

            direction_result = get_direction(
                result[0],
                result[1],
                result[2],
                result[3]
            )
            return get_result(direction_result)

        else:
            return "no face detected"

    except AttributeError as e:
        print(e)
        return "image read error, please check your image path"
