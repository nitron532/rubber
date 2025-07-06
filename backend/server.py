from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import subprocess
import os


app = Flask(__name__)
@app.route('/') #might want to link this function to a button call from front end instead of onload of /
def test():
    # return jsonify({"rah": "hello world"})
    tryTex = subprocess.run(
        ["./texlive/bin/windows/pdflatex", "-interaction=nonstopmode", "template.tex"],
        cwd="./files",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    other_files = [x for x in os.listdir("./files") if x != '150.tex' and x!='template.tex' and x != '157.tex']
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