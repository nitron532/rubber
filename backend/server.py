from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename
import subprocess
import os


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
CORS(app, origins = "http://localhost:5173") 
@app.route('/submit', methods = ['POST'])
def compile():
    file = request.files['file']
    filename = secure_filename(file.filename)
    root,extension = os.path.splitext(filename)
    result = {"compiled": "unknown", "out": "none", "err": "none", "name":filename}
    print(extension)
    if extension != ".tex":
        result["compiled"] = "no"
        result["err"] = "this isn't a latex file..."
        return jsonify(result)
    destination="/".join(["./files", filename])
    file.save(destination)
    with open(f"./files/template.tex", 'r') as f:
        data = f.readlines()
    data[6] = f'\\input{{{filename}}}\n'
    with open(f"./files/template.tex", 'w') as f:
        f.writelines(data)
        #might want to erase the write after this so there is no trace of write afterwards(security?)
    tryTex = subprocess.run(
        ["./texlive/bin/windows/pdflatex", "-interaction=nonstopmode", "template.tex"],
        cwd="./files",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    other_files = [x for x in os.listdir("./files") if x!='template.tex']
    pdf = True if "template.pdf" in other_files else False
    for file in other_files:
        os.remove(f"./files/{file}")
    result["compiled"] = "yes" if pdf else "no"
    #should probably remove all the crap in stderror if there is an error so it can be condensed, but keep full error in case needed
    if not pdf:
        result["out"] = tryTex.stdout.decode("utf-8")
        result["err"] = tryTex.stderr.decode("utf-8")
    return jsonify(result)


if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5000, debug=True) #might have to change to something similar to gauchogrub 