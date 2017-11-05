import sys
import argparse
import os.path

from PIL import Image


class SizeCalculator:

    def __init__(self, size):
        self.initial_width, self.initial_height = size
        self.initial_proportion = self.initial_width / self.initial_height
        self.width, self.height = self.initial_width, self.initial_height
        self.proportion = self.initial_proportion

    def __str__(self):
        return '{}x{}'.format(int(self.width), int(self.height))

    @property
    def size(self):
        return int(self.width), int(self.height)

    @property
    def proportion_changed(self):
        return self.proportion != self.initial_proportion

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
        self.width, self.height = width, height
        self.proportion = self.width / self.height

    def calculate(self, scale, width, height):
        if scale:
            self._by_scale(scale)
            return

        if width and height:
            self._by_width_height(width, height)
            return

        if width:
            self._by_width(width)

        if height:
            self._by_height(height)


def resize_image(imagepath, scale, width, height, output):

    image = Image.open(imagepath)

    calculator = SizeCalculator(image.size)
    calculator.calculate(scale, width, height)

    result_image = image.resize(calculator.size, Image.ANTIALIAS)

    image_filename = output
    if not output:
        filename, file_ext = os.path.splitext(imagepath)
        image_filename = '{}__{}{}'.format(filename, calculator, file_ext)

    result_image.save(image_filename)

    return calculator.proportion_changed


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='image resizer')
    parser.add_argument('imagepath', help='source image path')
    parser.add_argument('--width', help='result image width', type=int)
    parser.add_argument('--height', help='result image height', type=int)
    parser.add_argument('--scale', help='result image scale', type=float)
    parser.add_argument('--output', help='result image path')
    args = parser.parse_args()

    if not args.scale and not args.width and not args.height:
        print('No one resize option has set')
        print('Run script with [--width, --height | --scale] options')
        sys.exit()

    if args.scale and args.width or args.scale and args.height:
        print('Options conflict:')
        print('\t--width or --height are not compatible with --scale')
        sys.exit()

    if resize_image(
        args.imagepath,
        args.scale,
        args.width,
        args.height,
        args.output
    ):
        print('WARNING: Image proportion has changed')
