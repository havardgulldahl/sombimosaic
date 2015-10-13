#encoding:utf-8
#

from wand.image import Image


if __name__ == '__main__':
  import sys
  with Image(sys.argv[1]) as original:
    with original.convert('png') as converted:
      converted.trim(color=None, fuzz=0.33)
      converted.save(filename='trimd.png')