from grammar import Grammar
from Parser import ParserRecursiveDescendent

pr=ParserRecursiveDescendent("Lab5/g1.txt","Lab5/seq.txt","Lab5/myout.txt")
pr.run(pr.sequence)

print(str(pr))