import sys
import argparse

from PIL import Image


class ArgumentStorage:

    def __init__(self):
        parser = argparse.ArgumentParser(description='image resizer')

        parser.add_argument(
            'source_image',
            help='path to source image',
            type=str
        )

        parser.add_argument('--width', help='result image width', type=int)
        parser.add_argument('--height', help='result image height', type=int)
        parser.add_argument('--scale', help='result image scale', type=float)
        parser.add_argument('--output', help='path to result image', type=str)
        arguments = parser.parse_args()
        self.source_image = arguments.source_image
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
            self.proportion_changed = not proportion == self.proportion
            self.width = width
            self.height = height


if __name__ == '__main__':

    arguments = ArgumentStorage()

    if not arguments.has_width and not arguments.has_height and not arguments.has_scale:
        sys.exit('Image will not be resized, because no one resize option is sets')

    if (arguments.has_width or arguments.has_height) and arguments.has_scale:
        sys.exit('Options conflict: width or height are not compatible with scale')

    image = Image.open(arguments.source_image)
    size_calculator = SizeCalculator(image.size)

    if arguments.has_scale:
        size_calculator.calculate(scale=arguments.scale)

    elif not arguments.has_width:
        size_calculator.calculate(height=arguments.height)

    elif not arguments.has_height:
        size_calculator.calculate(width=arguments.width)

    else:
        size_calculator.calculate(width=arguments.width, height=arguments.height)

        if size_calculator.proportion_changed:
            print('WARNING: Image proportion changes')

    result_image = image.resize(size_calculator.size)

    if arguments.has_output:
        result_image.save(arguments.output)

    else:
        image_filename = 'xxx.jpg'
        result_image.save(image_filename)
