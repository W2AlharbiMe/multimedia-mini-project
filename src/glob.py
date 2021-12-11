'''
any global configurations, methods goes here
'''

from . import app
from flask import (render_template)


### App configurations


## shortcut to render a template
def render(name, ctx):
  # custom template extension
  ext = 'html.jinja2'
  return render_template("{0}.{1}".format(name, ext), context=ctx)
