from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import subprocess



app = Flask(__name__)

@app.route('/')
def test():
    # return jsonify({"rah": "hello world"})
    result = subprocess.run(
        ["./texlive/bin/windows/pdflatex", "-interaction=nonstopmode", r"./files/157.tex"]
    )
    #remove tex.log file thats created after running somehow? import os
    return jsonify(result.returncode)



if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5000, debug=True) #might have to change to something similar to gauchogrub 