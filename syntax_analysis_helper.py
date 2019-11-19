'''-------------------------------------------------------------------------------------
AUTHORS			:	Brian Chung & Michael Cingari & Owen Salcido
LAST MODIFIED	:	11/18/2019
FILE            :   'syntax_analysis_helper.py'
-------------------------------------------------------------------------------------'''

#Given errorID and token, return an error code
def syntaxError(errorID, token):
    if(errorID == "S"):
        if(token == "end"):
            return("Only use ; if there is a next statement")
        else:
            return("Not a valid statement.")
    elif(errorID == "A"):
        return("Not a valid assignment.")
    elif(errorID == "E"):
        return("Not a valid expression.")
    elif(errorID == "E'"):
        return("Not a valid expression.")
    elif(errorID == "T"):
        return("Not a valid term.")
    elif(errorID == "T'"):
        return("Not a valid term.")
    elif(errorID == "F"):
        return("Not a valid factor.")
    elif(errorID == "D"):
        return("Not a valid declarative.")
    elif(errorID == "P"):
        return("Not a valid type.")
    elif(errorID == "Mi"):
        return("Not a valid ID")
    elif(errorID == "I"):
        return("Not a valid if statement")
    elif(errorID == "L"):
        return("Not a valid else statement")
    elif(errorID == "W"):
        return("Not a valid while statement")
    elif(errorID == "B"):
        return("Not a valid begin statement")
    elif(errorID == "Ms"):
        return("Not a valid statement")
    elif(errorID == "C"):
        return("Not a valid conditional")
    elif(errorID == "C'"):
        return("Not a valid conditional")
    elif(errorID == "R"):
        return("Not a valid relational operator")
    else:
        return("Unknown error")

#Convert shortened rule into readable format
def convertRule(ruleID):
    if(ruleID == "S"):
        return("<Statement>")
    elif(ruleID == "A"):
        return("<Assignment>")
    elif(ruleID == "E"):
        return("<Expression>")
    elif(ruleID == "E'"):
        return("<Expression Prime>")
    elif(ruleID == "T"):
        return("<Term>")
    elif(ruleID == "T'"):
        return("<Term Prime>")
    elif(ruleID == "F"):
        return("<Factor>")
    elif(ruleID == "D"):
        return("<Declarative>")
    elif(ruleID == "P"):
        return("<Type>")
    elif(ruleID == "Mi"):
        return("<More IDs>")
    elif(ruleID == "I"):
        return("<If Statement>")
    elif(ruleID == "L"):
        return("<Else Statement>")
    elif(ruleID == "W"):
        return("<While Statement>")
    elif(ruleID == "B"):
        return("<Block Statement>")
    elif(ruleID == "Ms"):
        return("<More Statements>")
    elif(ruleID == "C"):
        return("<Conditional>")
    elif(ruleID == "C'"):
        return("<Conditional Prime>")
    elif(ruleID == "R"):
        return("<Relational Operator>")
    elif(ruleID == "ID"):
        return("<Identifier>")
    else:
        return(ruleID)

#Output a printable format of the full production rule given pop and push values during stack parsing
def printProductionRules(poppedValue, pushValues):
    outputString = "  "
    outputString += convertRule(poppedValue) + " -> "
    for values in pushValues:
        outputString += convertRule(values) + " "
    return(outputString)