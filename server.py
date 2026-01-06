import time
import subprocess
import os
import sys
import shutil
from pathlib import Path
from checker import check
passedCheck = True
"""
this file size limit will need to vary depending on usage: for feeding to model, it will have to be large, as we are
uploading around 1000+ files from oldrepo to the thing. once it's in use by teaching team, it will have to be smaller
"""

# copy directory to some working directory. loop thru each and check. try minimize io operations

questionFolderPath = Path(sys.argv[1])
glob_path = questionFolderPath.glob("*") 

def compile():
    #resets globals per compile
    global passedCheck
    fileNameList = []
    compileList = []
    guidelineList = []
    errorList = []
    result = {"compiledFiles": compileList, "fileNames":fileNameList, "passedFiles": guidelineList, "errors": errorList}
    nestedPath = Path(f"{questionFolderPath}/files")
    nestedPath.mkdir(parents=True, exist_ok=True)
    currentTime = str(time.time())
    templateFileName = f"template{currentTime[:currentTime.find('.')]}.tex"
    totalPath = Path(f"{nestedPath}/{templateFileName}")
    with open(totalPath, 'w') as f:
        f.writelines(["\\documentclass{article}\n","\\usepackage{format\n}",\
                      "\\usepackage{mc_bubble}\n","\\usepackage{magicswitch}\n","\\begin{document}\n","\\input{}\n","\\end{document}\n"])

    for file in glob_path:
        passedCheck = False
        folder, filename = os.path.split(file)

        if(filename == "files"):continue

        result["fileNames"].append(filename)
        root,extension = os.path.splitext(filename)
        if extension != ".tex":
            result["compiledFiles"].append(False)
            result["passedFiles"].append(False)
            result["errors"].append(f"{filename} isn't a latex file.")
        else:
            with open(totalPath, 'r') as f:
                data = f.readlines()
            data[5] = f'\\input{{../{filename}}}\n' #5th line is input env in template tex file
            with open(totalPath, 'w') as f:
                f.writelines(data)
            #might want to erase the write after this so there is no trace of write afterwards(security?)
            tryTex = subprocess.run(
                ["./texlive/bin/windows/pdflatex", "-interaction=nonstopmode", templateFileName],
                cwd=nestedPath,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            pdf = os.path.exists(os.path.join(nestedPath, f"{templateFileName[:templateFileName.find(".")]}.pdf"))
            print(f"{filename} compiled? ", pdf)
            if pdf:
                result["compiledFiles"].append(True)
                passedCheck = check(Path(f"{questionFolderPath}/{filename}")) #returns boolean
            else:
                result["compiledFiles"].append(False)
                result["passedFiles"].append(False)
            print("passed check?: ", passedCheck)
            print()
            result["passedFiles"].append(passedCheck)
    shutil.rmtree(nestedPath)
    print(result)
    return result


compile()
