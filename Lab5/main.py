from grammar import Grammar
from Parser import ParserRecursiveDescendent

pr=ParserRecursiveDescendent("Lab5/g2.txt","pif.out","Lab5/myout.txt")
pr.run(pr.sequence)

print(str(pr))