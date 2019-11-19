'''-------------------------------------------------------------------------------------
AUTHORS			:	Brian Chung & Michael Cingari & Owen Salcido
LAST MODIFIED	:	11/18/2019
FILE            :   'main.py'
-------------------------------------------------------------------------------------'''

import pandas as pd
from collections import deque
from finitestatemachine import FiniteStateMachine
from digit_transistions import digit_integerStateTransistions, digit_realStateTransistions, digit_StartTransistions
from identifier_transistions import ident_FirstStateTransistions, ident_StartTransistions, ident_ValidIdentifierStateTransistions
from syntax_analysis_helper import syntaxError, convertRule, printProductionRules

#Set debug to true to view stack data in terminal
debug = True

#Used pandas to read in csv table to perform LL Table parser
table_df = pd.read_csv("Table-Predictive-Parser.csv", delimiter=",", encoding="utf-8-sig")
table_df.set_index("TOS", inplace = True)
terminal_list = table_df.columns.values

#Print if debug is true
if (debug == True):
    print("DEBUG MODE ENABALED")
    print("Read in CSV - LL Parsing Table:")
    print(table_df)

#Initialize data structures
SyntaxStack = deque() #Holds syntax/production rules (LL Stack)
LexemeDeque = deque() #Holds lexeme or remaining input
stackView = [] #Stack view is only used if debug is true

#Create list of keywords, operators, and seperators
keyword_list = ["int", "float", "bool", "if", "else", "then", "endif", "while", "whileend", "do", "doend", "for", "forend", "input", "output", "and", "or", "function", "begin", "end"]
operator_list = ["=", "+", "-", "*", "/", "%","<", ">", "<=", ">=", "==", "!=", "++", "--"]
seperator_list = [";", ":", ",", "(", ")", "{", "}", "[", "]","'",".","$"]

#The split operators function deals with any cases such as "a+b-c" and splits it into "a + b - c" for the other functions to recieve correct format
def insertSpace(inputLine):
    #Add whitespace char at end of string in case last element in a operator
    leftToParseString = inputLine + ' '     #String that has not yet parsed
    parsedString = ''                       #String that is already parsed
    while(len(leftToParseString) != 0):
        #If first two elements of string left ot parse is a 2 char operator
        if(leftToParseString[:2] == "++" or leftToParseString[:2] == "--"
            or leftToParseString[:2] == "<=" or leftToParseString[:2] == ">="
            or leftToParseString[:2] == "==" or leftToParseString[:2] == "!="):
            parsedString = parsedString + ' ' + leftToParseString[:2] + ' '
            tempString = leftToParseString[2:]
            leftToParseString = tempString
        #If next char in string is an operator/seperator
        elif(leftToParseString[0] == "!" or leftToParseString[0] == "="
        or leftToParseString[0] == "+" or leftToParseString[0] == "-"
        or leftToParseString[0] == "*" or leftToParseString[0] == "/"
        or leftToParseString[0] == "<" or leftToParseString[0] == ">"
        or leftToParseString[0] == "(" or leftToParseString[0] == ")"
        or leftToParseString[0] == "{" or leftToParseString[0] == "}"
        or leftToParseString[0] == "[" or leftToParseString[0] == "]"
        or leftToParseString[0] == ":" or leftToParseString[0] == ";"
        or leftToParseString[0] == ","):
            parsedString = parsedString + ' ' + leftToParseString[0] + ' '
            tempString = leftToParseString[1:]
            leftToParseString = tempString
        #Else shift next string
        else:        
            parsedString = parsedString + leftToParseString[0]
            leftToParseString = leftToParseString[1:]
    return parsedString


def lexur(lexeme):
    #Check if keyword:
    if any(item == lexeme for item in keyword_list):
        return(lexeme, "KEYWORD")
    else:
        #split along list of operator/seperator and run function with the new list of strings
        lexeme = insertSpace(lexeme)
        for splitLex in lexeme.split():
            #Check if operator:
            if any(item == splitLex for item in operator_list):
                return(splitLex, "OPERATOR")
            #Check if seperator:
            elif any(item == splitLex for item in seperator_list):
                return(splitLex, "SEPERATOR")     
            #Check for idenitifier/digit
            else:
                tempLexeme = splitLex
                splitLex = splitLex + '~'
                splitLex = " ".join(splitLex)
                if(splitLex[0].isdigit() or splitLex[0] == "."):
                    return(tempLexeme, digitMachine.run(splitLex))
                elif(splitLex[0].isalpha() or splitLex[0] == "_"):
                    return(tempLexeme, identMachine.run(splitLex))
                else:
                    return(tempLexeme, "UNKNOWN")

#DRIVER FUNCTIONS AKA MAIN
#Read input.txt to perform lexical analysis
if __name__ == "__main__":

    #Add Digit Finite State Machine States
    digitMachine = FiniteStateMachine()
    digitMachine.add_state("digit_Start", digit_StartTransistions)
    digitMachine.add_state("digit_integerState", digit_integerStateTransistions)
    digitMachine.add_state("digit_realState", digit_realStateTransistions)
    digitMachine.add_state("digit_errorState", None, end_state=1)
    digitMachine.add_state("INT", None, end_state=1)
    digitMachine.add_state("REAL", None, end_state=1)
    digitMachine.set_start("digit_Start")

    #Add Identifier Finite State Machine States
    identMachine = FiniteStateMachine()
    identMachine.add_state("ident_State", ident_StartTransistions)
    identMachine.add_state("ident_firstState", ident_FirstStateTransistions)
    identMachine.add_state("ident_ValidIdentifierState", ident_ValidIdentifierStateTransistions)
    identMachine.add_state("ident_errorState", None, end_state=1)
    identMachine.add_state("ID", None, end_state=1)
    identMachine.set_start("ident_State")

    #If debug is true append table headers to the stack view
    if (debug == True):
        stackView.append('{0:<30} {1:<30} {2:<30}'.format("Stack","Input","Action"))


    codeHolder = ""
    syntacticallyCorrect = True
    printToken = True

    with open("input.txt", "r") as inputFile:
        for line in inputFile:
            #If line is empty pass
            if(not line.strip()):
                pass
            #If the line begins with a ! or a comment symbol, skip line and do not compile
            elif((line.lstrip())[0] == '!'):
                pass
            #Else run syntactic analysis
            else:
                codeHolder += line
        SyntaxStack.append("$")         #Push $ onto the stack
        codeHolder = codeHolder + " $"  #Put end-of-file marker ($) at the end of the input string
        SyntaxStack.append("S")         #Push (Starting Symbol) on to the stack
        lexeme = insertSpace(codeHolder)#Insert space in lexeme where appropriate
        lexeme.strip()                  #Strip extraneous spaces
        multipleLex = lexeme.split()    #Split lexeme into multiple lexeme

        #For every lexeme in multipleLex assign lexeme list with either the actual token or lexeme
        for lexeme in multipleLex:
            tempList = lexur(lexeme)
            #If token is operator/seperator, keep op/sep as the token
            if (tempList[1] == "OPERATOR" or tempList[1] == "SEPERATOR" or tempList[1] == "KEYWORD"):
                LexemeDeque.append(tempList[0])
            else:
                LexemeDeque.append(tempList[1])
                     
        #Create/open output.txt to output production rules
        outPutFile = open("output.txt", "w")

        #While stack not empty do
        while (len(SyntaxStack) > 0):
            #Debug Station:
            debugList = ["","",""]
            debugList[0] = "".join(SyntaxStack)
            debugList[1] = "".join(LexemeDeque)

            #let terminal = TOS symbol and i=incoming token
            terminal = SyntaxStack[-1] #Peek last element in deque or top of stack
            incomingToken = LexemeDeque[0] #Peek first element in deque or front of queue

            #Print incoming token if print token bool is true
            if(printToken):
                outPutFile.write("Incoming Token: " + incomingToken + "\n")
                printToken = False

            if any(item == terminal for item in terminal_list):
                if (terminal == incomingToken):
                    debugList[2] += "pop(" + SyntaxStack.pop() + ")"
                    debugList[2] += ", lexur() popped " + LexemeDeque.popleft()
                    printToken = True   #Print token to true so next iteration, token will print

                else:
                    syntacticallyCorrect = False
                    outPutFile.write("ERROR! Terminal did not match expected terminal" + "\n")
                    outPutFile.write("  Recieved: " + LexemeDeque.popleft() + "  Expected: " + SyntaxStack.pop() + "\n")
                    break   #Do not continue to compile
            else:
                #if Table[t,i] has entry then
                if (str(table_df.loc[terminal, incomingToken]) != "nan"):
                    poppedValue = SyntaxStack.pop()
                    debugList[2] += "pop(" + poppedValue + ")" #Output to debug
                    pushValues = list() #push Table[t,i] in reverse order
                    lookUp = table_df.loc[terminal, incomingToken]
                    pushValues = lookUp.split() #Split look up value by whitespace
                    outPutFile.write(printProductionRules(poppedValue, pushValues) + "\n") #Print Production Rules
                    pushValues.reverse() #Reverse order of list of TOS
                    debugList[2] += ", push(" #Output to debug
                    for values in pushValues:
                        debugList[2] += values
                        #If Eplison, do not append into values
                        if (str(table_df.loc[terminal, incomingToken]) != "ε"):
                            SyntaxStack.append(values)
                        debugList[2] += ")" #Output to debug
                else:
                    syntacticallyCorrect = False
                    outPutFile.write("Syntactically incorrect" + "\n")
                    outPutFile.write("ERROR! Parsing Table Defaulted." + "\n")
                    outPutFile.write(syntaxError(SyntaxStack.pop(), LexemeDeque.popleft()) + "\n")
                    break   #Do not continue to compile

            if (debug == True):
                stackView.append('{0:30} {1:<30} {2:<30}'.format(debugList[0],debugList[1],debugList[2]))

        #Reset Deque
        LexemeDeque.clear()

        #If debug is true print stack view in terminal
        if(debug == True):
            for line in stackView:
                print(line)

        #If the input is syntactically correct output:
        if(syntacticallyCorrect == True):
            print("Accepted! Stack is empty with no input remaining.")
            print("Please view output.txt to view all production rules used!")
            outPutFile.write("Accepted! Code is Syntactically Correct!")

        outPutFile.close()
