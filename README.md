# Image Resizer

Script image_resize.py resize image in accordance with script options

# Script options

Run script with --help option to show help info

```bash
$ python image_resize.py --help
usage: image_resize.py [-h] [--width WIDTH] [--height HEIGHT] [--scale SCALE]
                       [--output OUTPUT]
                       image

image resizer

positional arguments:
  imagepath            source image path

optional arguments:
  -h, --help       show this help message and exit
  --width WIDTH    result image width
  --height HEIGHT  result image height
  --scale SCALE    result image scale
  --output OUTPUT  result image path
```

# Requirements

python 3.5+  
See requirements.txt for dependence

# Using examples

```bash
$ python image_resize.py image.jpg --scale 0.8 --output images/scaled.png
$ python image_resize.py image.jpg --width 1920
$ python image_resize.py image.png --height 1080 --output images/image_1080.png
$ python image_resize.py image.jpg --width 100 --height 100 
WARNING: Image proportion has changed
$ python image_resize.py image.jpg 
No one resize option has set
Run script with [--width, --height | --scale] options
$ python image_resize.py image.jpg --scale 0.8 --height 200
Options conflict:
	--width or --height are not compatible with --scale
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
