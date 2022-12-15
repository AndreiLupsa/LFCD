from SymbolTable import SymbolTable
import re
import sys
from Utils import Utils

reserved_words = ["incepe", "intreg", "citeste", "daca", "si", "afiseaza","radical","rational", "pentru"]
reserved_ops = [",", "!=" , "<", "<=", ">", ">=","<==","[", "]", "{", "}", ";", ":", "(", ")","%","+","/","="]

class PIF:
    def __init__(self):
        self.__data = []

    def __setitem__(self, key, pos):
        self.__data.append((key, pos))
    
    def __str__(self):
        return "\n".join(map(str, self.__data))

    def __getitem__(self,token):
        return self.__data[token]
    
    def tokens(self):
        return list(map(lambda x: x[0], self.__data))

def is_constant_or_identifier(token,finite_automata):
    return finite_automata.isAccepted(token)

    # def is_constant_or_identifier(token,finite_automata):
    # try:
    #     int(token)
    #     return re.match(r"^([+-][^0]|[0-9])", token)
    # except:
    #     return re.match(r"^[0-9]", token) is None and \
    #             (re.match(r'^".+"$', token) is not None \
    #                 or re.match(r"^`.+`$", token) is not None \
    #                 or re.match(r"^'.'$", token) is not None \
    #                 or re.match(r'^[^`\'"]+$', token))
    # return True

def lexical_analyser(path,finite_automata):
    pif = PIF()
    st = SymbolTable(100)
    with open(path) as f:
        i=0
        line_i = 1
        line = f.readline()
        while line:
            #print(line)
            split = re.findall(r'`.+`|".+"|\'.\'|[,{}:;()\[\]\.\+\-\*/=!<>%@|&\(\)]|[^,{}:;()\s\[\]\.\+\-\*/=!<>%@|&\(\)]+', line) #[a-zA-Z]+
            split = list(filter(lambda x: x is not None and x != '', map(lambda x: x.strip(), split)))
            #print(split)
            i=0
            while i < len(split) - 1:
                if split[i] in ('=', '!', '<', '>', '+', '-', '*', '/'):
                    if split[i + 1] == '=':
                        split[i] += '='
                        del split[i + 1]
                        if split[i]=='<=' and split[i+1]=='=':
                            split[i]+='='
                            del split[i+1]
                i += 1
            i = 0
            for token in split:
                if token in reserved_words or token in reserved_ops:
                    pif[token] = -1
                elif is_constant_or_identifier(token,finite_automata):
                    st.add(token,i)
                    pif['id'] = st.get(token)
                    i+=1
                else:
                    raise Exception("Lexical error. Invalid token: '{}' on line {}".format(token, line_i))
            line = f.readline()
            line_i += 1
    return st, pif
    


if __name__ == "__main__":
    finite_automata = Utils.readFromFile('Lab4/FAInt.in')
    st, pif = lexical_analyser('Lab3/p1.txt',finite_automata)
    # st, pif = lexical_analyser('Lab3/p2.txt',finite_automata)
    
    with open("st.out", "w+") as f:
        f.write(str(st))

    with open("pif.out", "w+") as f:
        f.write(str(pif))

    print("Valid program!")


    