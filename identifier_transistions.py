'''-------------------------------------------------------------------------------------
AUTHORS			:	Brian Chung & Michael Cingari & Owen Salcido
LAST MODIFIED	:	11/18/2019
FILE            :   'identifier_transistions.py'
-------------------------------------------------------------------------------------'''

# The character '~' or tilde represents the end of a idenitifer or digit, it is used to jump to an end state

#Identifier State Transitions
def ident_StartTransistions(inputString):
    splitInputString = inputString.split(None,1)
    inputChar, inputString = splitInputString if len(splitInputString) > 1 else (inputString,"")
    #If first char is an alphabetic go to first state
    if(inputChar.isalpha()):
        newState = "ident_firstState"
    #If first char is an 'underscore' go to first state
    elif(inputChar == "_"):
        newState = "ident_firstState"
    #Else first char is not an alphabetic or a '_', therefore go to error state
    else:
        newState = "ident_errorState"
    return(newState, inputString)

def ident_FirstStateTransistions(inputString):
    splitInputString = inputString.split(None,1)
    inputChar, inputString = splitInputString if len(splitInputString) > 1 else (inputString,"")
    #If char is a '~', go to end idenitifer state
    if(inputChar == "~"):
        newState = "ID"
    #If char is an alphabetic go to valid identiifer state
    elif(inputChar.isalpha()):
        newState = "ident_ValidIdentifierState"
        #If char is a digit go to valid identiifer state
    elif(inputChar.isdigit()):
        newState = "ident_ValidIdentifierState"
    #If char is an 'underscore'(_) go to valid identiifer state
    elif(inputChar == "_"):
        newState = "ident_ValidIdentifierState"
    #If char is an 'dollar sign'($) go to valid identiifer state
    elif(inputChar == "$"):
        newState = "ident_ValidIdentifierState"
    #Else char is not an alphabetic, digit, '_', or '$', therefore go to error state
    else:
        newState = "ident_errorState"
    return(newState, inputString)

def ident_ValidIdentifierStateTransistions(inputString):
    splitInputString = inputString.split(None,1)
    inputChar, inputString = splitInputString if len(splitInputString) > 1 else (inputString,"")
    #If char is a '~', go to end idenitifer state
    if(inputChar == "~"):
        newState = "ID"
    #If char is an alphabetic go to valid identiifer state
    elif(inputChar.isalpha()):
        newState = "ident_ValidIdentifierState"
        #If char is a digit go to valid identiifer state
    elif(inputChar.isdigit()):
        newState = "ident_ValidIdentifierState"
    #If char is an 'underscore'(_) go to valid identiifer state
    elif(inputChar == "_"):
        newState = "ident_ValidIdentifierState"
    #If char is an 'dollar sign'($) go to valid identiifer state
    elif(inputChar == "$"):
        newState = "ident_ValidIdentifierState"
    #Else char is not an alphabetic, digit, '_', or '$', therefore go to error state
    else:
        newState = "ident_errorState"
    return(newState, inputString)