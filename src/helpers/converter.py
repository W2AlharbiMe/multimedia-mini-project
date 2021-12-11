from PIL import Image
from .validate import get_file_extension


def png_processor(image, path):
  try:
    # discard alpha channel, convert image from RGBA to RGB
    rgb_img = image.convert('RGB')

    # save image
    rgb_img.save(path)

    return True
  except:
    return False


def converter_process(uploaded_file_path, name, _to):
  save_path = 'public/converted/{0}/{1}.{0}'.format(_to, name)

  # try to open the image
  image = Image.open(uploaded_file_path)

  extension = get_file_extension(uploaded_file_path)

  # if the image extension is png run png processor
  if extension == 'png':
    png_processor(image, save_path)
  else:
    image.save(save_path)
  

  return save_path
