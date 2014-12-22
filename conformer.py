from mutagen.mp4 import MP4, MP4Cover
from PIL import Image
from cStringIO import StringIO
import os, argparse, shutil

TARGET_COVER_DIMENSIONS = 400, 400
OSX_SPECIAL_DIRECTORIES = ".Trashes", ".Spotlight-V100", ".fseventsd"

def read_first_cover(mp4):
  covers = mp4['covr']
  if covers:
    return covers[0]

def save_first_cover(mp4, raw_image):
  cover = MP4Cover(raw_image, MP4Cover.FORMAT_JPEG)
  mp4['covr'][0] = cover
  mp4.save()

def create_image_from_string(image_data):
  image_buffer = StringIO(image_data)
  return Image.open(image_buffer)

def is_image_within_dimensions(image, dimensions):
  return image.size <= dimensions

def is_mpeg4_audio(filename):
  return filename.endswith(".m4a")

def resize(image, size):
  image.thumbnail(size, Image.ANTIALIAS)
  return image

def create_raw_jpeg(image):
  jpeg_image_buffer = StringIO()
  image.save(jpeg_image_buffer, "JPEG")
  return jpeg_image_buffer.getvalue()

def is_hidden(filename):
  return filename.startswith(".")

args_parser = argparse.ArgumentParser()
args_parser.add_argument("directory")
args_parser.add_argument("--remove-hidden-files", default = False, action = "store_true", help = "remove files starting with a '.'")
args_parser.add_argument("--remove-osx-special-directories", default = False, action = "store_true", help = "remove directories " + str(OSX_SPECIAL_DIRECTORIES))
args = args_parser.parse_args()

if args.remove_osx_special_directories:
  for dir in OSX_SPECIAL_DIRECTORIES:
    absolute_dir_path = os.path.join(args.directory, dir)
    if os.path.exists(absolute_dir_path):
      print "removing OSX special directory " + dir
      shutil.rmtree(absolute_dir_path)

for dirpath, subdirs, files in os.walk(args.directory):
  for file in files:
    filename = os.path.join(dirpath, file)
    if is_hidden(file) and args.remove_hidden_files:
      print "removing hidden file " + filename
      os.remove(filename)
    if is_mpeg4_audio(file):
      mp4 = MP4(filename)
      raw_cover = read_first_cover(mp4)
      if raw_cover:
        image = create_image_from_string(raw_cover)
        if is_image_within_dimensions(image, TARGET_COVER_DIMENSIONS):
          print "skipping " + filename + " beacuse it is already within target size " + str(TARGET_COVER_DIMENSIONS)
        else:
          image = resize(image, TARGET_COVER_DIMENSIONS)
          raw_image = create_raw_jpeg(image)
          print "saving " + filename + " with size " + str(image.size)
          save_first_cover(mp4, raw_image)
      else:
        print "no cover found in " + filename
