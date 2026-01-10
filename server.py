import subprocess
import os
import sys
import shutil
import math
from pathlib import Path
from checker import check
import multiprocessing

counter = 0
cores = os.process_cpu_count()
questionFolderPath = Path(sys.argv[1])
glob_path = questionFolderPath.glob("*")
globFiles = [f for f in glob_path if f.__str__().find(".tex") != -1]
nestedPath = Path(f"{questionFolderPath}/files")
nestedPath.mkdir(parents=True, exist_ok=True)
perProc = math.ceil(len(globFiles) / cores)

def sub_process_compile(globFiles):
    localCount = 0
    print("starting process: ", os.getpid())
    passedCheck = False
    fileNameList = []
    compileList = []
    guidelineList = []
    errorList = []
    result = {"compiledFiles": compileList, "fileNames":fileNameList, "passedFiles": guidelineList, "errors": errorList}
    templateFileName = f"template{os.getpid()}.tex"
    totalPath = Path(f"{nestedPath}/{templateFileName}")
    with open(totalPath, 'w') as f:
        f.writelines(["\\documentclass{article}\n","\\usepackage{format\n}",\
                      "\\usepackage{mc_bubble}\n","\\usepackage{magicswitch}\n","\\begin{document}\n","\\input{}\n","\\end{document}\n"])

    for file in globFiles:
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
            # print(f"{filename} compiled? ", pdf)
            if pdf:
                result["compiledFiles"].append(True)
                passedCheck = check(Path(f"{questionFolderPath}/{filename}")) #returns boolean
            else:
                result["compiledFiles"].append(False)
                result["passedFiles"].append(False)
            # print("passed check?: ", passedCheck)
            # print()
            result["passedFiles"].append(passedCheck)
            if passedCheck: localCount += 1
            passedCheck = False
    # print(result)
    return result, localCount

def main():
    global counter
    results = []
    with multiprocessing.Pool(cores) as p:
        results = p.starmap(sub_process_compile, [([globFiles[perProc * i: perProc *(i+1)]]) for i in range(cores)])
    shutil.rmtree(nestedPath)
    for r in results: counter += r[1]
    print(f"Passed / Total: {counter} / {len(globFiles)} ")

if __name__ == "__main__":
    main()