from . import app
from .glob import render
from flask import (request, flash, redirect, url_for, send_file)
from .helpers.upload import (save_file)
from .helpers.converter import converter_process
from .helpers.validate import early_report, get_file_extension, validate_formats


@app.route("/", methods=["GET"])
def index():
    ctx = {
      "active": "home"
    }

    return render('index', ctx)




@app.route("/downloads/<id>", methods=["GET"])
def generate_download_link(id):
  ext = get_file_extension(id)
  return send_file('public/converted/{0}/{1}'.format(ext,id), as_attachment=True)


@app.route("/converter", methods=["GET", "POST"])
def converter():
  ctx = {
    "active": "converter"
  }

  # handle post request
  if request.method == 'POST':
    values = request.values

    # get formats
    _from = get_file_extension(request.files['image'].filename)
    _to = values['to']
    
    # START ---- validation process ----

    # early report 
    if early_report(request, 'image'):
      flash("<span class='text-danger'>you didn't provide any image.</span>")
      return redirect(url_for('converter'))


    ## validate formats
    validation_result, message = validate_formats(_from, _to)

    if not validation_result:
      flash(message)

      return redirect(url_for('converter'))
    
    # END ---- validation process ----
    

    # START ---- save process ----
    result, name, path, message = save_file(request, _from)
    # END ---- save process ----


    # START ---- convert process ----
    # if the file is saved successfully
    if result:
      # run converter processor
      converter_process(path, name, _to)

    # END ---- convert process ----

    # START ---- finalize process ----

    a_tag = f"<a href='{url_for('generate_download_link', id=f'{name}.{_to}')}' class='btn btn-primary btn-sm'>Click here to download.</a>"
    message = message.format(a_tag)
    flash(['success', message], 'success')
    return redirect(url_for('converter'))
    # END ---- finalize process ----

  return render('app', ctx)


print(
'''
     .    .     __  __     .    .___  ____   _                                                                  
    /|    /     |   |     /|    /   \ /   \  |                                                                  
   /  \   |     |___|    /  \   |__-' |,_-<  |                                                                  
  /---'\  |     |   |   /---'\  |  \  |    ` |                                                                  
,'      \ /---/ /   / ,'      \ /   \ `----' /                                                                  
                                                                                                                
                                         .____   ___   .___                                                     
                                         /     .'   `. /   \                                                    
                                         |__.  |     | |__-'                                                    
                                         |     |     | |  \                                                     
                                         /      `.__.' /   \                                                    
                                                                                                                
   _____ _      _   _____  _______ .____  __   __                                                               
  (       `.   /   (      '   /    /      |    |                                                                
   `--.     `./     `--.      |    |__.   |\  /|                                                                
      |     ,'         |      |    |      | \/ |                                                                
 \___.'  _-'      \___.'      /    /----/ /    /                                                                
                                                                                                                
                               .___   .____  __    __ .____  .       ___   .___  __   __ .____  __    _  _______
                               /   `  /      |     |  /      /     .'   `. /   \ |    |  /      |\   |  '   /   
                               |    | |__.    \    /  |__.   |     |     | |,_-' |\  /|  |__.   | \  |      |   
                               |    | |        \  /   |      |     |     | |     | \/ |  |      |  \ |      |   
                               /---/  /----/    \/    /----/ /---/  `.__.' /     /    /  /----/ |   \|      /
''')