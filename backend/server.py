from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename
import subprocess
import os
from checker import check
passedCheck = True

app = Flask(__name__)
"""
this file size limit will need to vary depending on usage: for feeding to model, it will have to be large, as we are
uploading around 1000+ files from oldrepo to the thing. once it's in use by teaching team, it will have to be smaller
"""
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #16 MB
CORS(app, origins = "http://localhost:5173") 
@app.route('/submit', methods = ['POST'])
def compile():
    global passedCheck
    fileNameList = []
    compileList = []
    guidelineList = []
    result = {"compiledFiles": compileList, "fileNames":fileNameList, "passedFiles": guidelineList}
    
    for i in range(len(request.files)):
        passedCheck = True
        file = request.files[f"filesList[{i}]"]
        filename = secure_filename(file.filename)
        result["fileNames"].append(filename)
        root,extension = os.path.splitext(filename)
        if extension != ".tex":
            result["compiledFiles"].append(False)
        destination="/".join(["./files", filename])
        file.save(destination)
        with open(f"./files/template.tex", 'r') as f:
            data = f.readlines()
        data[6] = f'\\input{{{filename}}}\n' #6th line is input env in template.tex
        with open(f"./files/template.tex", 'w') as f:
            f.writelines(data)
        #might want to erase the write after this so there is no trace of write afterwards(security?)
        tryTex = subprocess.run(
            ["./texlive/bin/windows/pdflatex", "-interaction=nonstopmode", "template.tex"],
            cwd="./files",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        other_files = [x for x in os.listdir("./files") if x!='template.tex'] #might wanna clean up after entire process is run instead of each time
        pdf = True if "template.pdf" in other_files else False
        if pdf:
            result["compiledFiles"].append(True)
        else:
            result["compiledFiles"].append(False)
        if result["compiledFiles"][i]:
            passedCheck = check(os.path.join("files", filename)) #returns boolean
        for file in other_files:
            os.remove(f"./files/{file}")
        result["passedFiles"].append(passedCheck)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5000, debug=True) #might have to change to something similar to gauchogrub 