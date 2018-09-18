import math
import cv2

from .imageprocessing import cv2_to_face_recognition

from PIL import Image
import face_recognition as fr
import numpy as np

def get_face_location(fr_img_array):
    """
    This function takes in an array of images that can be 
    used in face_recognition and returns a list of tuples 
    of found face locations in css (top, right, bottom, left) 
    order like [(171, 409, 439, 141)]
    """
    return fr.api.face_locations(fr_img_array)

def image_pre_processing(cv_img_array):
    """
    This function preprocesses images (resizes it) and returns
    an image array of the face and eye coordinates
    """
    if cv_img_array.shape[1] > 500:
        cv_img_array = cv2.resize(cv_img_array, (0, 0), fx=0.4, fy=0.4)

    fr_img_array = cv2_to_face_recognition(cv_img_array)
    face_location = get_face_location(fr_img_array)

    if face_location:
        cv_img_array = cv_img_array[
            face_location[0][0]:face_location[0][2],
            face_location[0][3]:face_location[0][1]
        ]

        eye_locations = get_eye_locations(fr_img_array, face_location)

        for i in range(6):
            height = eye_locations["left_eye"][i][0] - face_location[0][3]
            width = eye_locations["left_eye"][i][1] - face_location[0][0]
            eye_locations["left_eye"][i] = (height, width)

        for i in range(6):
            height = eye_locations["right_eye"][i][0] - face_location[0][3]
            width = eye_locations["right_eye"][i][1] - face_location[0][0]
            eye_locations["right_eye"][i] = (height, width)

        result = {"cv_img_array": cv_img_array, "eye_locations": eye_locations}
        return result

    else:
        return None


def get_pupil_position(width, height, center):
    """
    This function returns a number that indicates the position of the pupil
    """
    width_trisection = int(width / 3)
    height_trisection = int(height / 3)

    if (center["x"] < width_trisection) and \
            (center["y"] < height_trisection):
        return 0
    elif (center["x"] > width_trisection * 2) and \
        (center["y"] < height_trisection):
        return 2
    elif center["y"] < height_trisection:
        return 1
    elif (center["x"] < width_trisection) and \
        (center["y"] > height_trisection * 2):
        return 6
    elif (center["x"] > width_trisection * 2) and \
        (center["y"] > height_trisection * 2):
        return 8
    elif center["y"] > height_trisection * 2:
        return 7
    elif center["x"] < width_trisection:
        return 3
    elif center["x"] > width_trisection * 2:
        return 5
    else:
        return 4

def get_eye_direction(cv_img_array, eye_locations):
    """
    This function takes in an array of images that can be used in
    OpenCV and eye coordinates to return the position of both
    eyes and the proportion of effective pixels used to determine
    the position of the eyeball
    """
    # adjust brightness and contrast
    cv_img_array = np.uint8(np.clip(1.1 * cv_img_array + 30, 0, 255))

    left_coordinate = get_eye_rectangle_coordinates(eye_locations["left_eye"])
    right_coordinate = get_eye_rectangle_coordinates(eye_locations["right_eye"])

    left_eyeball = get_eyeball_location(cv_img_array, left_coordinate)
    left_percent = left_eyeball["percent"]
    left_result = left_eyeball["pupil_direction"]

    right_eyeball = get_eyeball_location(cv_img_array, right_coordinate)
    right_percent = right_eyeball["percent"]
    right_result = right_eyeball["pupil_direction"]

    return [left_result, left_percent, right_result, right_percent]

def get_eye_locations(fr_img_array, face_location):
    """
    This function takes in an image as a numpy array, the location
    of the face, and returns a dictionary that contains the locations
    of both eyes
    """
    face_landmarks = fr.api.face_landmarks(
        fr_img_array,
        face_locations=face_location
    )

    if face_landmarks:
        left_eye = face_landmarks[0]["left_eye"]
        right_eye = face_landmarks[0]["right_eye"]
        eye_locations = {"left_eye": left_eye, "right_eye": right_eye}
        return eye_locations

    else:
        return None

def get_eye_rectangle_coordinates(eye_landmarks):
    """
    This function takes in the output of face_landmarks from 
    the face_recognition library and returns the coordinates of 
    the eye rectangle
    """
    width = eye_landmarks[3][0] - eye_landmarks[0][0]
    height = int((eye_landmarks[4][1] + eye_landmarks[5][1] - \
                  eye_landmarks[1][1] - eye_landmarks[2][1]) / 2)

    x = eye_landmarks[0][0]
    y = int((eye_landmarks[1][1] + eye_landmarks[2][1]) / 2)

    return {"x1": x, "y1": y, "x2": x + width, "y2": y + height}

def get_eyeball_location(cv_image_array, eye_coordinate):
    """
    This function returns the position of the eyeball in the
    eye rectangle. It takes in a image read by OpenCV, the
    coordinates returned by get_eye_rectangle_coordinates(), and
    returns the ratio of effective pixels used to determine the
    position of the eyeball to the total. It also returns the coordinates
    to the pupil of the eyeball, and the position of the pupil
    via get_eye_rectangle_coordinates()
    """

    eyeball_roi = cv_image_array[
        eye_coordinate["y1"]:eye_coordinate["y2"],
        eye_coordinate["x1"]:eye_coordinate["x2"]
    ]

    # convert to grayscale
    eyeball_roi = cv2.cvtColor(eyeball_roi, cv2.COLOR_BGR2GRAY)

    gray_val_total = 0  # grayscale vals total of pixels in eye rectangle
    gray_val_min = 255  # minimum of all pixel gray vals in eye rectangle

    for i in range(eyeball_roi.shape[0]):  # height
        for j in range(eyeball_roi.shape[1]):  # width
            gray_val_total += eyeball_roi[i][j]
            if gray_val_min > eyeball_roi[i][j]:
                gray_val_min = eyeball_roi[i][j]

    # get average of the gray values of all pixels in the eye rectangle
    gray_val_avg = int(
        gray_val_total / (eyeball_roi.shape[0] * eyeball_roi.shape[1])
    )

    eyeball_center_x = 0
    eyeball_center_y = 0
    counter = 0

    if ((gray_val_avg * 2) / 3) > gray_val_min:
        for i in range(eyeball_roi.shape[0]):  # height
            for j in range(eyeball_roi.shape[1]):  # width
                if eyeball_roi[i][j] <= ((gray_val_avg * 2) / 3):
                    eyeball_center_y += i
                    eyeball_center_x += j
                    counter += 1

    # if the gray value of one pixel is less than 2/3 of the gray average,
    # then the minimum value is used
    else:
        for i in range(eyeball_roi.shape[0]):  # height
            for j in range(eyeball_roi.shape[1]):  # width
                if eyeball_roi[i][j] <= gray_val_min:
                    eyeball_center_y += i
                    eyeball_center_x += j
                    counter += 1

    # calculate the proportion of valid pixels used to determine
    # the position of the eyeball
    percent = counter / (eyeball_roi.shape[0] * eyeball_roi.shape[1])

    eyeball_center_x = math.ceil(eyeball_center_x / counter)
    eyeball_center_y = math.ceil(eyeball_center_y / counter)

    pupil_position = {"x": eyeball_center_x, "y": eyeball_center_y}
    pupil_direction = get_pupil_position(
        eyeball_roi.shape[1],
        eyeball_roi.shape[0],
        pupil_position
    )

    return {"percent": percent,
            "pupil_position": pupil_position,
            "pupil_direction": pupil_direction}

