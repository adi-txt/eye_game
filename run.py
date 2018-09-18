import sys

from pkg.parser import get_eyeball_direction

def main() -> None:
    if len(sys.argv) == 1:
        return("No images submitted.")
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
