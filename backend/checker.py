from TexSoup import TexSoup
passedCheck = True
envCount = {}
"""
store envs / commands in a dict (to support nested characteristic)
this way i can easily check if an environment contains something / doesn't contain something
once stored in a dict, check() itself will see if it passes, then return the status to server.py
base level of dict can be treated as document environment since every file lives inside document env from template.tex
"""
def storeAsDict(s): #ignores BraceGroup inside verbatim for code
    global envCount
    structure = {}
    for section in s.contents:
        #store text from code{} so I can check it in check()
        if hasattr(section, 'name') and section.name != "BraceGroup":
            envCount.setdefault(section.name, 0)
            envCount[section.name]+=1
            if envCount[section.name] > 1:
                structure[f"{section.name}{envCount[section.name]}"] = storeAsDict(section)
            else:
                structure[f"{section.name}1"] = storeAsDict(section)
    return structure

def displayInOrder(d, indent=0): # for test purposes
    for key, value in d.items():
        print(" " * indent + f"begin {key}")
        if isinstance(value, dict):
            displayInOrder(value, indent + 4)
        else:
            print(" " * (indent + 4) + str(value))

def checkTree(tree): 
#this will grow as i add more requirements ( next one to do is code{} and what it contains, length? whitespace? to 
# check if its just used for question description or (bad) in place of verbatim)
    global passedCheck
    #might wanna split these conditions
    if "AnswerArea" not in envCount or "Solution" not in envCount:
        print("AnswerArea or Solution not found in tex file!")
        passedCheck = False
        return
    elif envCount["AnswerArea"] != 1 or envCount["Solution"] != 1:
        print(envCount["AnswerArea"], envCount["Solution"])
        passedCheck = False
        return
    for key,value in tree.items():
        if key.contains("AnswerArea") and not value:
            passedCheck = False
            return
        elif key.contains("Question"):
            passedCheck = False
            return
        if isinstance(value, dict):
            checkTree(value)


def check(pa):
    with open(pa) as p:
        soup = TexSoup(p.read())
        tree = storeAsDict(soup)
        print(tree)
        if not tree:
            return False #empty dict
        #one pass loop to iterate through tree in order of insertion (item has to be first )
        for section in tree:
            if section != "item1":
                print("item not found")
                return False
            break
        checkTree(tree)
        return passedCheck #could return more info since i already have specific error checks


"""
!!needs multiple file input!!
process:
check guideline in here:
actual guideline checking stays inside of this file !done
return response (yes or no) to server.py !done
server will append checker result to response object and send to frontend !done
front end needs to display followsFormat status

guidelines:
certain amount of specific environments (must be specific amount or fail check) !done
if any deprecated/banned environments found (question, code outside of item) fail check !done
somehow fail vertical spaces instead of using the vspace command

must begin with item command
only one solution environment
only one answer environment, red flag if a bunch of newlines are used instead of vspace
if code{} found, check for whitespace or long length to raise red flag

"""

