#Brian Chung
#9/27/2019

# The character '~' or tilde represents the end of a idenitifer or digit, it is used to jump to an end state

#Digit State Transistions
def digit_StartTransistions(inputString):
    splitInputString = inputString.split(None,1)
    inputChar, inputString = splitInputString if len(splitInputString) > 1 else (inputString,"")
    #If first char is a digit, go to integer state
    if(inputChar.isdigit()):
        newState = "digit_integerState"
    #If first char is a digit, go to real/float state
    elif(inputChar == "."):
        newState = "digit_realState"
    #Else first char is not a digit or a '.', therefore go to error state
    else:
        newState = "digit_errorState"
    return(newState, inputString)

def digit_integerStateTransistions(inputString):
    splitInputString = inputString.split(None,1)
    inputChar, inputString = splitInputString if len(splitInputString) > 1 else (inputString,"")
    #If currently an integer and char is a '~', go to end integer state
    if(inputChar == "~"):
        newState = "INT"
    #If currently an integer and char is a digit, stay classified as an integer
    elif(inputChar.isdigit()):
        newState = "digit_integerState"
    #If currently an integer and char is a '.', go to real/float state
    elif(inputChar == "."):
        newState = "digit_realState"
    #Else char is not a digit or a '.', therefore go to error state
    else:
        newState = "digit_errorState"
    return(newState, inputString)

def digit_realStateTransistions(inputString):
    splitInputString = inputString.split(None,1)
    inputChar, inputString = splitInputString if len(splitInputString) > 1 else (inputString,"")
    #If currently an real/float and char is a '~', go to end real/float state
    if(inputChar == "~"):
        newState = "REAL"
    #If currently a real/float and char is a digit, stay classified as a real/float
    elif(inputChar.isdigit()):
        newState = "digit_realState"
    #Else (char is not a digit) go to error state
    else:
        newState = "digit_errorState"
    return(newState, inputString)