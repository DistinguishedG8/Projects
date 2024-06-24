
# -> * File State Application * <-

# -> Runs on Python 3.10
# -> The GUI must be installed be running use the following in command prompt:
# -> pip install customtkinter


# <*> Key Elements <*>

import re
import customtkinter

# -> Sets display style
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

# -> Creates root, main display format
root = customtkinter.CTk()
root.geometry("500x350")

# -> Master frame, ties in other elements
frame = customtkinter.CTkFrame(master = root)
frame.pack(pady = 20, padx = 60, fill = "both", expand = True)

# -> Main label header
header_Label = customtkinter.CTkLabel(master = frame, text = "File State", font = ("Calibri", 24))
header_Label.pack(pady = 12, padx = 10)


# <*> Functions <*>

# -> Function after user clicks accept
def accept_Button():
 

    # -> Regular expression to check against user email
    emailPattern = re.compile("^[a-zA-Z0-9]+[^a-zA-Z0-9]{1}[a-zA-Z]+[^a-zA-Z0-9]{1}[a-z]{3}$")

    # -> Declares Variables
    test = action_Label.cget("text")
    user_Email = ""
    user_Text = ""
    typeState = False
    emailState = False

    # -> Checks the state of a label, to verify user clicked button, which kick starts everything else
    if test == "":
        action_Label.configure(text = "Success!")
        test = "Success!"


    # -> Function to retreive user text values
    def textmonkey(passedValue):
        retreivedValue = passedValue.get("0.0", "end")
        return retreivedValue

    # -> Function to retreive user entered values
    def retreiver(passedValue):
        retreivedValue = passedValue.get()
        return retreivedValue

    # -> Function to sanitize user input
    def sanitized(user_input):
        cleaned_input = user_input.replace("?","0.A.0.Z.1.A").replace("&","0.A.1.A.1.A").replace("%","0.A.2.B.1.A").replace("*","0.A.3.C.1.A").replace("(","0.A.4.D.1.A").replace(")","0.A.5.E.1.A").replace("{","0.A.6.F.1.A").replace("}","0.A.7.G.1.A").replace("]","0.A.8.H.1.A").replace("[","0.A.9.I.1.A").replace(",","1.A.0.J.1.A").replace("<","1.A.1.K.1.A").replace(">","1.A.2.L.1.A").replace("!","1.A.3.M.1.A").replace("/","1.A.4.N.1.A").replace("\\","1.A.5.O.1.A").replace("|","1.A.6.P.1.A").replace("=","1.A.7.Q.1.A").replace("#","1.A.8.R.1.A").replace("^","1.A.9.S.1.A").replace("$","2.A.0.T.1.A").replace("@","2.A.1.U.1.A")
        return cleaned_input

    # -> Import function, set to read from file
    def openFile(fileOpener, accessMode, user_input, User_Email):
        with open(fileOpener, accessMode) as dataFile:

            # -> Writes to file
            if typeState == True and emailState == True:
                finalUser_Email = User_Email.replace("2.A.1.U.1.A", "@")
                finalUser_Input = user_input.replace("0.A.0.Z.1.A","?").replace("0.A.1.A.1.A","&").replace("0.A.2.B.1.A","%").replace("0.A.3.C.1.A","*").replace("0.A.4.D.1.A","(").replace("0.A.5.E.1.A",")").replace("0.A.6.F.1.A","{").replace("0.A.7.G.1.A","}").replace("0.A.8.H.1.A","]").replace("0.A.9.I.1.A","[").replace("1.A.0.J.1.A",",").replace("1.A.1.K.1.A","<").replace("1.A.2.L.1.A",">").replace("1.A.3.M.1.A","!").replace("1.A.4.N.1.A","/").replace("1.A.5.O.1.A","\\").replace("1.A.6.P.1.A","|").replace("1.A.7.Q.1.A","=").replace("1.A.8.R.1.A","#").replace("1.A.9.S.1.A","^").replace("2.A.0.T.1.A","$").replace("2.A.1.U.1.A", "@")
                dataFile.write("\n " + finalUser_Email + " - " + finalUser_Input)
                reader_Label.configure(text = "Success!")
            
            # -> Reads from file
            elif typeState == False and emailState == True:
                for steps in dataFile:
                    reader_Label.configure(text = " \n " + steps + " \n ")

            return dataFile

    # -> Function to check user entered a valid email
    def emailChecker(user_email):
        emailTest = emailPattern.match(user_email)
        if emailTest != None:
            print("-----------")

        return emailTest


    # <*> User Input <*>

    # -> Kick Start for the app
    for loopElement in range(1):
               
        # -> Loop to check for a valid email
        for emailLoop in range(1):

            user_Email = retreiver(entry_Email).lower()
            testedEmail = emailChecker(user_Email)

            if testedEmail != None:
                emailState = True
                break

            elif testedEmail == None: 
                reader_Label.configure(text = "Please enter a valid email")
                print("Please enter a valid email")

        # -> Request user data
        user_File = retreiver(entry_FileName)
        user_AccessMode = retreiver(entry_AccessMode).lower()

        # -> Checks if the user will be writing to the file
        if user_AccessMode == "w" or user_AccessMode == "w+" or user_AccessMode == "a":
            typeState = True
        if typeState == True:
            user_Text = textmonkey(entry_UserText)


        # -> Error handling for Sanitization function
        try:
            cleanUser_Email = sanitized(user_Email)
            cleanUser_File = sanitized(user_File)
            cleanUser_AccessMode = sanitized(user_AccessMode)
            cleanUser_Text = sanitized(user_Text)
        except:
            # -> Clean input failed
            reader_Label.configure(text = " \nError C050: bad input\n ")
            print(" \nError C050: bad input\n ")

        # -> Error handling for openFile function
        try:
            # -> Passing user input into open file function
            openFile(cleanUser_File, cleanUser_AccessMode, cleanUser_Text, cleanUser_Email)
        except:
            # -> Failed to send user input to file function or file not found
            reader_Label.configure(text = " \nError F040: file failure\n ")
            print(" \nError F040: file failure\n ")
            
        if test == "Success!":
            action_Label.configure(text = "")    

    return


# <*> GUI Elements <*>

# -> Space for user email entry
entry_Email = customtkinter.CTkEntry(master = frame, placeholder_text = "Email")
entry_Email.pack(pady = 12, padx = 10)

# -> Space for selecting your file
entry_FileName = customtkinter.CTkEntry(master = frame, placeholder_text = "file.txt")
entry_FileName.pack(pady = 12, padx = 10)

# -> Displays file instructions
FileName_Label = customtkinter.CTkLabel(master = frame, text = "Please enter a file and the extension", font = ("Calibri", 12))
FileName_Label.pack(pady = 6, padx = 10)

# -> Space for selecting your access mode
entry_AccessMode = customtkinter.CTkEntry(master = frame, placeholder_text = "Access Mode")
entry_AccessMode.pack(pady = 12, padx = 10)

# -> Displays access mode options
AccessMode_Label = customtkinter.CTkLabel(master = frame, text = '(Append = "a", Read = "r", Overwrite = "w")', font = ("Calibri", 12))
AccessMode_Label.pack(pady = 6, padx = 10)

# -> Space for entering in your text
entry_UserText = customtkinter.CTkTextbox(master = frame)
entry_UserText.pack(pady = 12, padx = 10)

# -> Button Label Trigger
UserText_Label = customtkinter.CTkLabel(master = frame, text = "Enter your text above if writting", font = ("Calibri", 12))
UserText_Label.pack(pady = 6, padx = 10)

# -> Button for user login interaction
button = customtkinter.CTkButton(master = frame, text = "Update", command = accept_Button)
button.pack(pady = 12, padx = 10)

# -> Button Label Trigger
action_Label = customtkinter.CTkLabel(master = frame, text = "", font = ("Calibri", 12))
action_Label.pack(pady = 6, padx = 10)

# -> Label to display text to user
reader_Label = customtkinter.CTkLabel(master = frame, text = "", font = ("Calibri", 12))
reader_Label.pack(pady = 6, padx = 10)


root.mainloop()