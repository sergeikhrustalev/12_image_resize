import sys
import argparse


class ArgumentStorage:

    def __init__(self):
        parser = argparse.ArgumentParser(description='image resizer')
        parser.add_argument('source_path', help='path to source file', type=str)
        parser.add_argument('--width', help='result image width', type=int)
        parser.add_argument('--height', help='result image height', type=int)
        parser.add_argument('--scale', help='result image scale', type=float)
        parser.add_argument('--output', help='path to result image', type=str)
        arguments = parser.parse_args()
        self.source_path = arguments.source_path
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



if __name__ == '__main__':


    arguments = ArgumentStorage()


    if not arguments.has_width and not arguments.has_height and not arguments.has_scale:
        sys.exit('Image will not be resized, because no one resize option is sets')

    if (arguments.has_width or arguments.has_height) and arguments.has_scale:
        sys.exit('Options conflict: width or height are not compatible with scale')
    

    if arguments.has_scale:
        print('Creating new image with new scale')

    elif not arguments.has_width:
        print('New width will be calculated to save proportions')
        print('Creating new image')

    elif not arguments.has_height:
        print('New height will be calculated to save proportions')
        print('Creating new image')

    else:
        print('Creating image with new width x height')

    if arguments.has_output:
        print('Saving image to new directory')
    else:
        print('Saving image to current directory')





