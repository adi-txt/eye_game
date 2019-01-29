"""
This file deals with getting the direction of both eyeballs and
returning a final result based on the direction parsed.
"""


def get_direction(left_result, left_percent, right_result, right_percent):
    """
    This function judges the direction of gaze based on calculated percentages
    """
    if ((left_result == 4) and (right_result != 4)) or (
        (right_result == 4) and (left_result != 4)
    ):
        return right_result if left_result == 4 else left_result

    # pylint: disable=too-many-boolean-expressions, consider-using-in
    if ((left_result == 1) and ((right_result == 0) or (right_result == 2))) or (
        (right_result == 1) and ((left_result == 0) or (left_result == 2))
    ):
        return right_result if left_result == 1 else left_result

    # pylint: disable=too-many-boolean-expressions, consider-using-in
    if ((left_result == 7) and ((right_result == 6) or (right_result == 8))) or (
        (right_result == 7) and ((left_result == 6) or (left_result == 8))
    ):
        return right_result if left_result == 7 else left_result

    # pylint: disable=too-many-boolean-expressions, consider-using-in
    if ((left_result == 3) and ((right_result == 0) or (right_result == 6))) or (
        (right_result == 3) and ((left_result == 0) or (left_result == 6))
    ):
        return right_result if left_result == 3 else left_result

    # pylint: disable=too-many-boolean-expressions, consider-using-in
    if ((left_result == 5) and ((right_result == 2) or (right_result == 8))) or (
        (right_result == 5) and ((left_result == 2) or (left_result == 8))
    ):
        return right_result if left_result == 7 else left_result

    return right_result if left_percent < right_percent else left_result


# pylint: disable=too-many-return-statements
def get_result(result):
    """
    This function returns a direction based on judge_direction()
    """
    if result == 0:
        return "upper left"
    if result == 1:
        return "up"
    if result == 2:
        return "upper right"
    if result == 3:
        return "left"
    if result == 4:
        return "center"
    if result == 5:
        return "right"
    if result == 6:
        return "lower left"
    if result == 7:
        return "down"
    return "lower right"
