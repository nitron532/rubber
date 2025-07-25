import json
from TexSoup import TexSoup
environments = ["solution", "Solution", "verbatim", "Verbatim", "answerArea", "AnswerArea"]
commands = ["item", "Item", "vspace"]
passedCheck = True
answerAreaCount = 0 #needs to have a vspace in it
solutionCount = 0
"""
store envs / commands in a dict (to support nested characteristic)
this way i can easily check if an environment contains something / doesn't contain something
once stored in a dict, check() itself will see if it passes, then return the status to server.py
base level of dict can be treated as document environment since every file lives inside document env from template.tex
"""
def storeAsDict(s): #ignores BraceGroup inside verbatim for code
    structure = {}
    for section in s.contents:
        if hasattr(section, 'name') and section.name != "BraceGroup":
            structure[section.name] = storeAsDict(section)
    return structure


def displayInOrder(d, indent=0): # for test purposes
    for key, value in d.items():
        print(" " * indent + f"begin {key}")
        if isinstance(value, dict):
            displayInOrder(value, indent + 4)
        else:
            print(" " * (indent + 4) + str(value))

def checkTree(tree):
    global passedCheck, answerAreaCount, solutionCount
    for key,value in tree.items():
        if key == "AnswerArea":
            answerAreaCount+=1
            if "vspace" not in value: #\\vspace should be a key to an empty dict
                #guidelines mention another option of answerArea, will need to consider this (non empty space)
                print("vspace not found")
                passedCheck = False
                break
        elif key == "Solution":
            solutionCount+=1
        if isinstance(value, dict):
            checkTree(value)


def check(pa):
    global answerAreaCount, solutionCount
    answerAreaCount = 0
    solutionCount = 0
    with open(pa) as p:
        soup = TexSoup(p.read())
        tree = storeAsDict(soup)
        if not tree:
            return False #empty dict
        for section in tree:
            if section != "item":
                print("item not found")
                return False
            break
            #one pass loop to iterate through tree in order of insertion (item has to be first ), allow code env in item (For variables in question description)
        checkTree(tree)
        if answerAreaCount != 1 or solutionCount != 1:
            print(answerAreaCount)
            print(solutionCount)
            return False
        answerAreaCount = 0
        solutionCount = 0
        return passedCheck #could return more info since i already have specific error checks


"""
!!needs multiple file input!!
process:
check guideline in here:
actual guideline checking stays inside of this file !done
return response (yes or no) to server.py !done
server will append checker result to response object and send to frontend !done

guidelines:
certain amount of specific environments (must be specific amount or fail check) !done
if any deprecated/banned environments found (question, code outside of item) fail check
somehow fail vertical spaces instead of using the vspace command

must begin with item command
only one solution environment
only one answer environment, red flag if a bunch of newlines are used instead of vspace
if code{} found, check for whitespace or long length to raise red flag

"""


"""
def displayInOrder(s, indent =0):
    for section in s.contents:
        tabs = ""
        for i in range(indent):
            tabs += " "
        indent+=1
        if hasattr(section, 'name') and (section.name in environments or section.name in commands): #should probably only print sections that matter, also only prints beginnings, might need to print ends
            if section.name in environments:
                print(f"{tabs}begin {section.name}")
                displayInOrder(section, indent)
                print(f"{tabs}end {section.name}")
            elif section.name in commands:
                print(f"{tabs}{section.name}")
                displayInOrder(section,indent)
                """



