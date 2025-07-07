from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename
import subprocess
import os


app = Flask(__name__)
CORS(app, origins = "http://localhost:5173") 
@app.route('/submit', methods = ['POST'])
def compile():
    file = request.files['file']
    filename = secure_filename(file.filename)
    destination="/".join(["./files", filename])
    file.save(destination)
    with open(f"./files/template.tex", 'r') as f:
        data = f.readlines()
    data[6] = f'\\input{{{filename}}}\n'
    with open(f"./files/template.tex", 'w') as f:
        f.writelines(data)
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
    result = {"compiled": "unknown", "out": "none", "err": "none"}
    result["compiled"] = "yes" if pdf else "no"

    if not pdf:
        result["out"] = tryTex.stdout.decode("utf-8")
        result["err"] = tryTex.stderr.decode("utf-8")
    return jsonify(result)


if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5000, debug=True) #might have to change to something similar to gauchogrub 