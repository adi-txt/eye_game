'''
This is where the overall program is run.
'''
import os

from pkg.parser import get_eyeball_direction

def main() -> None:
    '''
    This is the main function
    '''

    path_to_images = os.path.join(os.getcwd(), 'images/')
    filenames = os.listdir(path_to_images)

    if filenames:

        for file in filenames:
            file_path = os.path.join(path_to_images, file)
            # print(file_path)
            try:
                direction = get_eyeball_direction(file_path)
            except: #pylint: disable=bare-except
                direction = "opencv cannot find eyeballs"

            print(
                "Image submitted: {0}, Eyeball direction: {1}".format(
                    file,
                    direction
                )
            )
    else:
        print("No images submitted")


if __name__ == '__main__':
    main()
