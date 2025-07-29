from TexSoup import TexSoup
passedCheck = True
envCount = {}

#base level of dict can be treated as document environment since every file lives inside document env from template.tex

def storeAsDict(s):
    global envCount, passedCheck
    structure = {}
    for section in s.contents:
        if hasattr(section, 'name') and section.name != "BraceGroup":
            envCount.setdefault(section.name, 0)
            envCount[section.name]+=1
            if section.name == "code":
                if any(c.isspace() for c in section.contents[0]):
                    passedCheck = False
                    return 
                structure[f"{section.name}{envCount[section.name]}"] = section.contents
            elif envCount[section.name] > 1:
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
#this will grow as i add more requirements
#if vspace is inside a solution (lowercase?) env, flag it as bad?
#new lines used instead of vspace is bad
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
        if "AnswerArea" in key and not value:
            passedCheck = False
            return
        elif "Question" in key:
            passedCheck = False
            return
        if isinstance(value, dict):
            checkTree(value)


def check(pa):# should try to return bool instead of using global
    global passedCheck
    global envCount
    #here, globals are reset each time check() is called (per file upload), 
    # so i don't need to reset them in helper functions which access globals since they've been reset before calling helpers
    envCount = {}
    passedCheck = True
    with open(pa) as p:
        soup = TexSoup(p.read())
        tree = storeAsDict(soup)
        if not tree:
            print("empty tex file")
            return False 
        elif not passedCheck:
            print("invalid use of code env (found a whitespace, code env should only be used to describe variables or functions in question description. Use verbatim for question code)")
            return False
        #one pass loop to iterate through tree in order of insertion (item has to be first )
        for key,value in tree.items():
            print(key)
            if key != "item1":
                print("item not found")
                return False
            break
        checkTree(tree)
        return passedCheck #could return more info since i already have specific error checks
    #maybe instead of passing a boolean i pass an object with boolean yes no passed check and a little error message since i print them out here already


"""
!!needs multiple file input!!
process:
check guideline in here:
actual guideline checking stays inside of this file !done
return response (yes or no) to server.py !done
server will append checker result to response object and send to frontend !done
front end needs to display followsFormat status

"""
