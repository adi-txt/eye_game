"""
This is where actual gaze direction parsing occurs.
"""
import cv2

from .functions import get_eye_direction, image_pre_processing
from .direction import get_direction, get_result


def get_eyeball_direction(image_path):
    """
    This utilizes various functions from functions.py and
    direction.py to get the gaze direction of a human
    subject in an image present at the given image path
    """
    # pylint: disable=no-member
    cv_img_array = cv2.imread(image_path)

    try:
        result = image_pre_processing(cv_img_array)

        if result is not None:
            result = get_eye_direction(result["cv_img_array"], result["eye_locations"])

            direction_result = get_direction(result[0], result[1], result[2], result[3])
            return get_result(direction_result)
        return "no face detected"

    except AttributeError as error:
        print(error)
        return "image read error, please check your image path"
