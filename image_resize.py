import sys
import argparse
import os.path

from PIL import Image


def get_arguments():

    parser = argparse.ArgumentParser(description='image resizer')
    parser.add_argument('image', help='source image path')
    parser.add_argument('--width', help='result image width', type=int)
    parser.add_argument('--height', help='result image height', type=int)
    parser.add_argument('--scale', help='result image scale', type=float)
    parser.add_argument('--output', help='result image path')
    args = vars(parser.parse_args())
    return {key: value for key, value in args.items() if value is not None}


class SizeCalculator:

    def __init__(self, size):
        self.width, self.height = size
        self.proportion = self.width / self.height
        self.proportion_changed = False

    def __str__(self):
        return '{}x{}'.format(int(self.width), int(self.height))

    @property
    def size(self):
        return int(self.width), int(self.height)

    def _by_scale(self, scale):
        self.width *= scale
        self.height *= scale

    def _by_width(self, width):
        self.width = width
        self.height = width / self.proportion

    def _by_height(self, height):
        self.height = height
        self.width = height * self.proportion

    def _by_width_height(self, width, height):
        proportion = width / height
        self.proportion_changed = proportion != self.proportion
        self.width = width
        self.height = height

    def calculate(self, arguments):

        if {'scale'} < set(arguments):
            self._by_scale(arguments['scale'])

        if {'width', 'height'} < set(arguments):
            self._by_width_height(arguments['width'], arguments['height'])
            return

        if {'width'} < set(arguments):
            self._by_width(arguments['width'])

        if {'height'} < set(arguments):
            self._by_height(arguments['height'])


if __name__ == '__main__':

    arguments = get_arguments()

    if not({'scale', 'width', 'height'} & set(arguments)):

        print('No one resize option has set')
        print('Run script with [--width, --height | --scale] options')
        sys.exit()

    if ({'scale', 'width'} < set(arguments) or
            {'scale', 'height'} < set(arguments)):

        print('Options conflict:')
        print('\t--width or --height are not compatible with --scale')
        sys.exit()

    image = Image.open(arguments['image'])
    calculator = SizeCalculator(image.size)
    calculator.calculate(arguments)

    if calculator.proportion_changed:
        print('WARNING: Image proportion has changed')

    result_image = image.resize(calculator.size)

    if {'output'} < set(arguments):
        result_image.save(arguments['output'])

    else:
        filename, file_ext = os.path.splitext(arguments['image'])
        image_filename = '{}__{}{}'.format(filename, calculator, file_ext)
        result_image.save(image_filename)
