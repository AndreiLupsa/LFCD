from grammar import Grammar
from texttable import Texttable
class ParserRecursiveDescendent:

    def __init__(self, grammar_file, sequence_file, out_file):

        self.grammar = Grammar(grammar_file)
        self.sequence = self.read_sequence(sequence_file)
        self.output_file = out_file
        self.tree = None

        # write file creation
        file = open(self.output_file, 'w')
        file.write("")
        file.close()

        print(self.sequence)
        print(self.grammar)

        # alpha - working stack, stores the way the parse is build
        self.working_stack = []

        # input stack
        self.input_stack = [self.grammar.initial_state]  # ['a', 'S', 'b', 'S', 'b', 'S']

        # q - normal state, b - back state, f - final state, e - error state
        self.state = "q"
        
        # i - position of current symbol in input sequenc
        self.index = 0

        # representation - parsing tree
        self.tree = []


    # reads the input sequence from the given file
    def read_sequence(self, sequence_file):

        sequence = []

        with open(sequence_file) as file:

            if sequence_file == "PIF.out":

                line = file.readline()
                line = file.readline()

                while line:
                    elems_line = line.split(" ")
                    sequence.append(elems_line[0])
                    line = file.readline()
            else:

                line = file.readline()
                while line:
                    sequence.append(line[0:-1])
                    line = file.readline()

        return sequence

    def write_all_data(self):

        with open(self.output_file, 'a') as file:

            file.write(str(self.state) + " ")
            file.write(str(self.index) + "\n")
            file.write(str(self.working_stack) + "\n")
            file.write(str(self.input_stack) + "\n")


    def write_in_output_file(self, message, final=False):

        with open(self.output_file, 'a') as file:
            if final:
                file.write("########RESULT:########\n")
            file.write(message + "\n")

    def expand(self):
        # when: head of input stack is a non terminal
        # (q, i, alpha, A beta) ⊢ (q, i, alpha A1, gamma1 beta)
        print("---expand---")
        self.write_in_output_file("---expand---")
        non_terminal = self.input_stack.pop(0) # pop A from beta
        self.working_stack.append((non_terminal, 0)) # alpha -> alpha A1
        new_production = self.grammar.productions_for_id(non_terminal)[0]
        print("1"+str(self.input_stack))
        self.input_stack = new_production.list[0] + self.input_stack
        print("2"+str(self.input_stack))
        

    def advance(self):
        # when: head of input stack is a terminal = current symbol from input
        # (q, i, alpha, a_i beta) ⊢ (q, i+1, alpha a_i, beta)
        print("---advance---")
        self.write_in_output_file("---advance---")
        self.working_stack.append(self.input_stack.pop(0))
        self.index += 1

    def momentary_insuccess(self):
        # when: head of input stack is a terminal != current symbol from input
        print("---momentary insuccess---")
        self.write_in_output_file("---momentary insuccess---")
        self.state = "b"

    def back(self):
        # when: head of working stack is a terminal
        # (b, i, alpha a, beta) ⊢ (b, i-1, alpha, a beta)
        print("---back---")
        self.write_in_output_file("---back---")
        new_thing = self.working_stack.pop()
        self.input_stack = [new_thing] + self.input_stack
        self.index -= 1
        # self.state = "b"

    def success(self):
        # print("---success---")
        self.write_in_output_file("---success---")
        self.state = "f"

    def another_try(self):
        # print("---another try---")
        self.write_in_output_file("---another try---")
        last = self.working_stack.pop()  # (last, production_nr)
        if last[1] + 1 < len(self.grammar.productions_for_id(last[0])[0].list):
            self.state = "q"
            # put working next production for the symbol
            new_tuple = (last[0], last[1] + 1)
            self.working_stack.append(new_tuple)
            
            # change production on top input
            length_last_production = len(self.grammar.productions_for_id(last[0])[0].list[last[1]]) #cate stergem
            # delete last production from input
            self.input_stack = self.input_stack[length_last_production:]

            # put new production in input
            new_production = self.grammar.productions_for_id(last[0])[0].list[last[1] + 1]
            self.input_stack = new_production + self.input_stack
        elif self.index == 0 and last[0] == self.grammar.initial_state: 
            print(self.index)
            self.state = "e"
        else: #go back
            # change production on top input
            length_last_production = len(self.grammar.productions_for_id(last[0])[0].list[last[1]])
            # delete last production from input
            self.input_stack = self.input_stack[length_last_production:]
            self.input_stack = [last[0]] + self.input_stack

    def print_working(self):
        # prints the working stack to the screen and in the output file
        print(self.working_stack)
        self.write_in_output_file(str(self.working_stack))

    def run(self, w):
        while (self.state != 'f') and (self.state != 'e'):
            self.write_all_data()
            if self.state == 'q':
                if len(self.input_stack) == 0 and self.index == len(w):
                    self.success()
                elif len(self.input_stack) == 0:
                    self.momentary_insuccess()
                elif self.input_stack[0] in self.grammar.nonterminals:
                    self.expand()
                    # WHEN: head of input stack is a non terminal

                elif self.index < len(w) and self.input_stack[0] == w[self.index]:
                    self.advance()
                else:
                    # WHEN: head of input stack is a terminal ≠ current symbol from input
                    self.momentary_insuccess()

            elif self.state == 'b':
                if self.working_stack[-1] in self.grammar.alphabet:
                    self.back()
                else:
                    self.another_try()

        if self.state == 'e':
            message = "ERROR! @ index: {}".format(self.index)
        else:
            message = "Sequence is accepted!"
            self.print_working()
        print(message)
        self.write_in_output_file(message, True)
        self.create_parsing_tree()

        # if self.state != "e":
        #     self.write_in_output_file("\nParsing tree: ")
        #     self.write_in_output_file("index info parent  left_sibling")
        #     for index in range(0, len(self.working_stack)):
        #         message = str(index) + "  " + str(self.tree[index])
        #         self.write_in_output_file(message)

    def create_parsing_tree(self):
        # creates the parsing tree
        local_table=[]
        fatherStack = [-1]
        local_index=1
        for index in range(0, len(self.working_stack)):
            # iterates in the working stack
            
            if(index==0):

                local_table.append((local_index,self.working_stack[index],fatherStack[-1], -1))
                fatherStack.pop()
                fatherStack.insert(0, local_index)
                local_index+=1
                father=fatherStack[0]
                productions = self.grammar.productions_for_id(self.working_stack[index][0])[0].list[self.working_stack[index][1]]
                for newindex in range(len(productions)):
                    
                    if(newindex==0):

                        if (productions[0] in self.grammar.alphabet):
                            whatToAdd=productions[0]
                            local_table.append((local_index, whatToAdd, father, -1))
                        else:
                            whatToAdd=(productions[0], self.working_stack[index][1])
                            local_table.append((local_index, whatToAdd, father, -1))
                            fatherStack.append(local_index)
                        
                        local_index+=1

                    else:

                        if (productions[newindex] in self.grammar.alphabet):
                            whatToAdd=productions[newindex]
                            local_table.append((local_index, whatToAdd, father, local_index-1))
                        else:
                            whatToAdd=(productions[newindex], self.working_stack[index][1])
                            local_table.append((local_index, whatToAdd, father, local_index-1))
                            fatherStack.append(local_index)
                            
                        local_index+=1

                fatherStack = fatherStack[1:]

            elif(type(self.working_stack[index]) == tuple):

                productions = self.grammar.productions_for_id(self.working_stack[index][0])[0].list[self.working_stack[index][1]]
                father=fatherStack[0]
                fatherStack=fatherStack[1:]

                newFathers = []

                for newindex in range(len(productions)):

                    if(newindex==0):

                        if (productions[0] in self.grammar.alphabet):
                            whatToAdd=productions[0]
                            local_table.append((local_index, whatToAdd, father, -1))
                        else:
                            whatToAdd=(productions[0], self.working_stack[index][1])
                            local_table.append((local_index, whatToAdd, father, -1))
                            newFathers.append(local_index)
                        
                        local_index+=1

                    else:

                        if (productions[newindex] in self.grammar.alphabet):
                            whatToAdd=productions[newindex]
                            local_table.append((local_index, whatToAdd, father, local_index-1))
                        else:
                            whatToAdd=(productions[newindex], self.working_stack[index][1])
                            local_table.append((local_index, whatToAdd, father, local_index-1))
                            newFathers.append(local_index)
                            
                        local_index+=1
                    
                fatherStack = newFathers + fatherStack
                
            else:
                continue

            self.tree = local_table

    def __str__(self):
        
        table = Texttable(1200)

        table.header(array=["INDEX", "ID", "PARENT", "LS"])

        for row in self.tree:
            table.add_row(array=[row[0], row[1], row[2], row[3]])
        
        return table.draw()

