ALLOWED_EXTENSIONS = {'bmp', 'dds', 'dib', 'png', 'jpg', 'jpeg', 'tga', 'webp'}

messages = {
  "errors": {
    "invalid_info": "<span class='text-danger'>you selected from: <strong>{0}</strong> but you uploaded image with extension <strong>{1}</strong>.</span>",
    "no_image": "<span class='text-danger'>you didn't provide any image.</span>",
    "formats_eq": "<span class='text-danger'>formats cannot be the same</span>",
    "required": "<span class='text-danger'>{0} field is required.</span>",
    "not_allowed": "<span class='text-danger'>Not allowed format.</span>"
  },
  "success": "<span class='text-success'>the image have been uploaded successfully {0}</span>"
}


def early_report(request, field):
  if 'image' not in request.files:
    return True

  filename = request.files[field].filename
  if filename == '':
    return True
  return False
  

def get_file_extension(filename):
 return filename.rsplit('.', 1)[1].lower()


def allowed_file(filename, _format='png'):
    return '.' in filename and \
           _format in ALLOWED_EXTENSIONS and \
           get_file_extension(filename) == _format


def validate_formats(_from, _to):
  is_from_allowed = _from in ALLOWED_EXTENSIONS
  is_to_allowed = _to in ALLOWED_EXTENSIONS

  if _from == _to:
    return [False, messages['errors']['formats_eq']]

  if _from == 'From':
    return [False, messages['errors']['required'].format('From')]

  if _to == 'To':
    return [False, messages['errors']['required'].format('To')]

  return [(is_from_allowed and is_to_allowed), messages['errors']['not_allowed']]
  

def validate_request(request, fieldName, _format='png'):
  field = request.files[fieldName]

  if early_report(request, fieldName):
    return [False, messages['errors']['no_image']]

  if field and allowed_file(field.filename, _format):
    return [True, messages['success']]

  message = messages['errors']['invalid_info'].format(_format, get_file_extension(field.filename))
  return [False, message]
