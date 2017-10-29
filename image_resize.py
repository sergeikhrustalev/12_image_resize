import sys
import argparse
import os.path

from PIL import Image


class ArgumentStorage:

    def __init__(self):

        parser = argparse.ArgumentParser(description='image resizer')
        parser.add_argument('image', help='source image path')
        parser.add_argument('--width', help='result image width', type=int)
        parser.add_argument('--height', help='result image height', type=int)
        parser.add_argument('--scale', help='result image scale', type=float)
        parser.add_argument('--output', help='result image path')
        arguments = parser.parse_args()

        self.image = arguments.image
        self.width = arguments.width
        self.height = arguments.height
        self.scale = arguments.scale
        self.output = arguments.output

    @property
    def has_width(self):
        return self.width is not None

    @property
    def has_height(self):
        return self.height is not None

    @property
    def has_scale(self):
        return self.scale is not None

    @property
    def has_output(self):
        return self.output is not None


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

    def calculate(self, width=None, height=None, scale=None):

        if width is None and height is None and scale is not None:
            self.width *= scale
            self.height *= scale

        if width is not None and height is None and scale is None:
            self.width = width
            self.height = width / self.proportion

        if width is None and height is not None and scale is None:
            self.height = height
            self.width = height * self.proportion

        if width is not None and height is not None and scale is None:

            if width == self.width and height == self.height:
                return

            proportion = width / height
            self.proportion_changed = proportion != self.proportion
            self.width = width
            self.height = height


if __name__ == '__main__':

    storage = ArgumentStorage()

    if all((
        not storage.has_width,
        not storage.has_height,
        not storage.has_scale
    )):

        print('No one resize option has set')
        print('Run script with [--width, --height | --scale] options')
        sys.exit()

    if (storage.has_width or storage.has_height) and storage.has_scale:

        print('Options conflict:')
        print('\t--width or --height are not compatible with --scale')
        sys.exit()

    image = Image.open(storage.image)
    calculator = SizeCalculator(image.size)

    if storage.has_scale:
        calculator.calculate(scale=storage.scale)

    elif not storage.has_width:
        calculator.calculate(height=storage.height)

    elif not storage.has_height:
        calculator.calculate(width=storage.width)

    else:
        calculator.calculate(width=storage.width, height=storage.height)

        if calculator.proportion_changed:
            print('WARNING: Image proportion has changed')

    result_image = image.resize(calculator.size)

    if storage.has_output:
        result_image.save(storage.output)

    else:
        filename, file_ext = os.path.splitext(storage.image)
        image_filename = '{}__{}{}'.format(filename, calculator, file_ext)
        result_image.save(image_filename)
