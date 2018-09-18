'''
This is where the overall program is run.
'''
import sys

from pkg.parser import get_eyeball_direction

def main() -> None:
    '''
    This is the main function
    '''
    if len(sys.argv) == 1:
        print("No images submitted.")
    else:
        for arg in sys.argv:
            if arg != 'run.py':
                print(
                    "Image submitted: {0}, Eyeball direction: {1}".format(
                        arg,
                        get_eyeball_direction(arg)
                    )
                )

if __name__ == '__main__':
    main()
