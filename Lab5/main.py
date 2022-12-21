from grammar import Grammar
from Parser import ParserRecursiveDescendent

pr = ParserRecursiveDescendent(
    "C:\\Users\\andre\\OneDrive\\Documents\\GitHub\\LFCD\\Lab5\\g1.txt",
    "C:\\Users\\andre\\OneDrive\\Documents\\GitHub\\LFCD\\seq.txt",
    "C:\\Users\\andre\\OneDrive\\Documents\\GitHub\\LFCD\\Lab5\\out1.txt")
pr.run(pr.sequence)

print(str(pr))
