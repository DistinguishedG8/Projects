
#*Error Handling Document Test*

import re

#Regular expression to check against user email
emailPattern = re.compile("^[a-zA-Z0-9]+[^a-zA-Z0-9]{1}[a-zA-Z]+[^a-zA-Z0-9]{1}[a-z]{3}$")

#Function to sanitize user input
def sanitized(user_input):
    cleaned_input = user_input.replace("?","0.A.0.Z.1.A").replace("&","0.A.1.A.1.A").replace("%","0.A.2.B.1.A").replace("*","0.A.3.C.1.A").replace("(","0.A.4.D.1.A").replace(")","0.A.5.E.1.A").replace("{","0.A.6.F.1.A").replace("}","0.A.7.G.1.A").replace("]","0.A.8.H.1.A").replace("[","0.A.9.I.1.A").replace(",","1.A.0.J.1.A").replace("<","1.A.1.K.1.A").replace(">","1.A.2.L.1.A").replace("!","1.A.3.M.1.A").replace("/","1.A.4.N.1.A").replace("\\","1.A.5.O.1.A").replace("|","1.A.6.P.1.A").replace("=","1.A.7.Q.1.A").replace("#","1.A.8.R.1.A").replace("^","1.A.9.S.1.A").replace("$","2.A.0.T.1.A").replace("@","2.A.1.U.1.A")
    return cleaned_input


#Import function, set to read from file
def openFile(fileOpener, accessMode, user_input, User_Email):
    with open(fileOpener, accessMode) as dataFile:

        #Writes to file
        if typeState == True:
            finalUser_Email = User_Email.replace("2.A.1.U.1.A", "@")
            finalUser_Input = user_input.replace("0.A.0.Z.1.A","?").replace("0.A.1.A.1.A","&").replace("0.A.2.B.1.A","%").replace("0.A.3.C.1.A","*").replace("0.A.4.D.1.A","(").replace("0.A.5.E.1.A",")").replace("0.A.6.F.1.A","{").replace("0.A.7.G.1.A","}").replace("0.A.8.H.1.A","]").replace("0.A.9.I.1.A","[").replace("1.A.0.J.1.A",",").replace("1.A.1.K.1.A","<").replace("1.A.2.L.1.A",">").replace("1.A.3.M.1.A","!").replace("1.A.4.N.1.A","/").replace("1.A.5.O.1.A","\\").replace("1.A.6.P.1.A","|").replace("1.A.7.Q.1.A","=").replace("1.A.8.R.1.A","#").replace("1.A.9.S.1.A","^").replace("2.A.0.T.1.A","$").replace("2.A.1.U.1.A", "@")
            dataFile.write("\n " + finalUser_Email + " - " + finalUser_Input)
        
        #Reads from file
        elif typeState == False:
            for steps in dataFile:
                print(" \n " + steps + " \n ")

        return dataFile


#Function to check user entered a valid email
def emailChecker(user_email):
    emailTest = emailPattern.match(user_email)
    if emailTest != None:
        print("-----------")

    return emailTest
 

#Declares Variables
user_Email = ""
user_Text = ""
typeState = False
emailState = False

#Loop to check for a valid email
while emailState == False:

    user_Email = input(" \nEnter your email \n (example@email.com): ").lower()
    testedEmail = emailChecker(user_Email)

    if testedEmail != None:
        emailState = True
        break

    elif testedEmail == None: 
        print("Please enter a valid email")

#Request user data
user_File = input(" \nEnter the file name with extension name \n (example.txt): ")
user_AccessMode = input(' \nEnter the Access Mode \n (Read - r, Write - w, Append - a): ').lower()

#Checks if the user will be writing to the file
if user_AccessMode == "w" or user_AccessMode == "w+" or user_AccessMode == "a":
    typeState = True
if typeState == True:
    user_Text = input(" \nEnter the text you want to write: \n \n ")


#Error handling for Sanitization function
try:
    cleanUser_Email = sanitized(user_Email)
    cleanUser_File = sanitized(user_File)
    cleanUser_AccessMode = sanitized(user_AccessMode)
    cleanUser_Text = sanitized(user_Text)
except:
    #Clean input failed
    print(" \nError C050: bad input\n ")

#Error handling for openFile function
try:
    #Passing user input into open file function
    openFile(cleanUser_File, cleanUser_AccessMode, cleanUser_Text, cleanUser_Email)
except:
    #Failed to send user input to file function or file not found
    print(" \nError F040: file failure\n ")

print("\n ")