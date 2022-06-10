import os, os.path
import datetime
import subprocess
from time import sleep
from traceback import print_exc
from flask import Flask, request
from flask import jsonify, render_template
try:
    from . import config
    from .jsonFileReader import ConfigFileReader
except:
    import config
    from jsonFileReader import ConfigFileReader
    
    
def sidebar_run_python_file(file_name): 
    file_path = ConfigFileReader().getMenuPythonFilePath(file_name=file_name)
    if os.path.exists(file_path):
        print((file_path)) 
        try:
            subprocess.Popen(["python", file_path])
        except:
            subprocess.Popen(["python3", file_path])
    return jsonify({})