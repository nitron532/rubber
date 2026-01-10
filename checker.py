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

def checkTree(tree, name): 
#this will grow as i add more requirements
#if vspace is inside a solution (lowercase?) env, flag it as bad?
    global passedCheck
    #might wanna split these conditions
    if "AnswerArea" not in envCount or "Solution" not in envCount:
        print(f"{name} : AnswerArea or Solution not found.")
        passedCheck = False
        return
    elif envCount["AnswerArea"] != 1 or envCount["Solution"] != 1:
        print(f"{name} : Found {envCount["AnswerArea"]} Answer Areas, and {envCount["Solution"]} Solutions.There should only be one of each.")
        passedCheck = False
        return
    for key,value in tree.items():
        if "AnswerArea" in key:
            if not value:
                passedCheck = False
                return
            for subkey, subvalue in value.items():
                if "verbatim" in subkey and len(subvalue.items()) == 0:
                    print(f"{name} : Verbatim found in Answer Area.")
                    passedCheck = False
                    return
        elif "Question" in key:
            passedCheck = False
            return
        if isinstance(value, dict):
            checkTree(value, name)


def check(pa):
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
            print(f"{p.name} : is an empty tex file.")
            return False 
        elif not passedCheck:
            print(f"{p.name} : Invalid use of code env (found a whitespace, code env should only be used to describe variables or functions in question description. Use verbatim for question code)")
            return False
        #one pass loop to iterate through tree in order of insertion (item has to be first )
        for key,value in tree.items():
            if key != "item1":
                print(f"{p.name} : Item not found.")
                return False
            break
        checkTree(tree,p.name)
        return passedCheck #could return more info since i already have specific error checks


