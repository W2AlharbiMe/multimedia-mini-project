import string
import random
from .validate import (validate_request)

def generate_new_name(length=10):
 return ''.join(random.choices(string.ascii_uppercase + string.digits, k = length))


def save_file(request, _format='png'):
  # generate a new name for the file 
  name = generate_new_name()

  # validate request
  result, message = validate_request(request, 'image', _format)


  # if everything is okay
  # save the image
  if result:

    # get image file from request
    image = request.files['image']

    # get image filename without extension
    filename = image.filename.rsplit('.', 1)[0].lower()
    # generate full name
    full_name = '{0}-{1}.{2}'.format(name, filename, _format)

    # generate the name for the conversion
    convert_name = '{0}-{1}'.format(name, filename)

    path = 'public/uploads/{0}/{1}'.format(_format, full_name)

    # save image in the path
    image.save(path)
  
    return [True, convert_name, path, message]

  return [False, '', '', message]


