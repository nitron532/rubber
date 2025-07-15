# import json
from TexSoup import TexSoup
import sys
# result = {
#     "status": "ok",
#     "sections": [],  # or whatever structure you want
# }
# path = sys.argv[1]
environments = ["solution", "Solution", "verbatim", "Verbatim", "answerArea", "AnswerArea"]
commands = ["item", "Item", "vspace"]
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

def check(pa):
    with open(pa) as p:
        soup = TexSoup(p.read())
        displayInOrder(soup)

# scp <your_name>@csil.cs.ucsb.edu:/cs/student/jrc974/new_repo/* .
