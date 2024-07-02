
# -> * File State Application * <-

# -> Runs on Python 3.10
# -> The GUI must be installed be running use the following in command prompt:
# -> pip install customtkinter


# <*> Key Elements <*>

# -> Imports
import re
import customtkinter
import os
import csv


# -> Sets display style
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

# -> Creates root, main display format
local_root = customtkinter.CTk()
local_root.geometry("500x350")

# -> Master frame, ties in other elements
local_frame = customtkinter.CTkFrame(master = local_root)
local_frame.pack(pady = 20, padx = 60, fill = "both", expand = True)

# -> Main label header
header_Label = customtkinter.CTkLabel(master = local_frame, text = "File State - Local Saves", font = ("Carlito", 24))
header_Label.pack(pady = 12, padx = 10)


# <*> Functions <*>

# -> Function after user clicks accept
def accept_Button():
 

    # -> Regular expression to check against user email
    emailPattern = re.compile("^[a-zA-Z0-9]+[^a-zA-Z0-9]{1}[a-zA-Z]+[^a-zA-Z0-9]{1}[a-z]{3}$")

    # -> Declares Variables
    label_State = action_flagLabel.cget("text")
    user_Email = ""
    user_Text = ""
    typeState = False
    emailState = False

    # -> Checks the state of a label, to verify user clicked button, which kick starts everything else
    if label_State == "":
        action_flagLabel.configure(text = "Success!")
        label_State = "Success!"

    # -> Function to retreive user text values
    def textmonkey(passedValue):
        retreivedValue = passedValue.get("0.0", "end")
        return retreivedValue

    # -> Function to retreive user entered values
    def retreiver(passedValue):
        retreivedValue = passedValue.get()
        return retreivedValue
    
    # -> Function to retreive file/folder name
    def file_retreiver(passedValue):
        retreivedValue = passedValue.cget("text")
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
            print("Vaild Email")

        return emailTest


    # <*> User Input <*>

    # -> Kick Start for the app
    for loopElement in range(1):
               
        # -> Loop to check for a valid email
        for emailLoop in range(1):

            user_Email = retreiver(entry_Email).lower()
            User_File = file_retreiver(file_flagLabel)
            testedEmail = emailChecker(user_Email)

            if testedEmail != None:
                emailState = True
                break

            elif testedEmail == None: 
                reader_Label.configure(text = "Please enter a valid email")
                print("Please enter a valid email")

        # -> Request user data
        user_AccessMode = retreiver(entry_AccessMode).lower()

        # -> Checks if the user will be writing to the file
        if user_AccessMode == "w" or user_AccessMode == "w+" or user_AccessMode == "a":
            typeState = True
        if typeState == True:
            user_Text = textmonkey(entry_UserText)


        # -> Error handling for Sanitization function
        try:
            cleanUser_Email = sanitized(user_Email)
            cleanUser_AccessMode = sanitized(user_AccessMode)
            cleanUser_Text = sanitized(user_Text)
        except:
            # -> Clean input failed
            reader_Label.configure(text = " \nError C050: bad input\n ")
            print(" \nError C050: bad input\n ")

        # -> Error handling for openFile function
        try:
            # -> Passing user input into open file function
            openFile(User_File, cleanUser_AccessMode, cleanUser_Text, cleanUser_Email)
        except:
            # -> Failed to send user input to file function or file not found
            reader_Label.configure(text = " \nError F040: file failure\n ")
            print(" \nError F040: file failure\n ")
            
        if label_State == "Success!":
            action_flagLabel.configure(text = "") 

    return

# -> Function to Display the found files/folders as tabs
def show_tab():
    stages = tab_view.get()
    file_flagLabel.configure(text = stages)
    
# -> Function to get the current directory files/folders
def show_FileFolders():
    # -> Checks current directory and objects within
    director = os.listdir()
    dataFromFile = csv.reader(director, delimiter = ",")
        
    # -> Displays folders and files
    for pointz in dataFromFile:
        comeTogether = "".join(pointz)
        tab_view.add(comeTogether)

def changePage_Button():
    test = 0


# <*> GUI Local File Page  <*>

# -> Button to switch to cloud view
button_changePage = customtkinter.CTkButton(master = local_frame, text = "Switch to Cloud", command = changePage_Button)
button_changePage.pack(pady = 10, padx = 10)

# -> File navigation tabs
tab_view = customtkinter.CTkTabview(master = local_frame, width = 100, height = 5, command = show_tab)
tab_view.pack(pady = 10, padx = 10)

# -> Space for user email entry
entry_Email = customtkinter.CTkEntry(master = local_frame, placeholder_text = "Email")
entry_Email.pack(pady = 10, padx = 10)

# -> Space for selecting your access mode
entry_AccessMode = customtkinter.CTkEntry(master = local_frame, placeholder_text = "Access Mode")
entry_AccessMode.pack(pady = 2, padx = 10)

# -> Displays access mode options
AccessMode_Label = customtkinter.CTkLabel(master = local_frame, text = '(Append = "a", Read = "r", Overwrite = "w")', font = ("Carlito", 14))
AccessMode_Label.pack(pady = 6, padx = 10)

# -> Space for entering in your text
entry_UserText = customtkinter.CTkTextbox(master = local_frame, height = 100 , width = 400)
entry_UserText.pack(pady = 2, padx = 10)

# -> Button for user accept interaction
button_accept = customtkinter.CTkButton(master = local_frame, text = "Accept", command = accept_Button)
button_accept.pack(pady = 10, padx = 10)

# -> Label to display text to user
reader_Label = customtkinter.CTkLabel(master = local_frame, text = "", font = ("Carlito", 24))
reader_Label.pack(pady = 6, padx = 10)


# <*> GUI Triggers  <*>

# -> Accept Button Label Trigger
action_flagLabel = customtkinter.CTkLabel(master = local_frame, text = "", font = ("Carlito", 12))
action_flagLabel.pack(pady = 1, padx = 1)

# -> Accept Button Label Trigger
file_flagLabel = customtkinter.CTkLabel(master = local_frame, text = "", font = ("Carlito", 1))
file_flagLabel.pack(pady = 1, padx = 1)


# <*> Starting Elements <*>

# -> Inserting fake text in textbox
entry_UserText.insert("0.0", "Enter Text Here")

# -> Kick Starts the tab labels, checking current files/folders
try:
    show_FileFolders()
except:
    print("Error could not show files")

local_root.mainloop()


# # <*> Cloud GUI Page <*>

# # -> Creates root, cloud display format
# cloud_root = customtkinter.CTk()
# cloud_root.geometry("500x350")

# # -> Master frame, ties in other elements
# cloud_frame = customtkinter.CTkFrame(master = cloud_root)
# cloud_frame.pack(pady = 20, padx = 60, fill = "both", expand = True)

# # -> Main label header
# cloudHeader_Label = customtkinter.CTkLabel(master = cloud_frame, text = "File State - Cloud Saves", font = ("Carlito", 24))
# cloudHeader_Label.pack(pady = 12, padx = 10)

# cloud_root.mainloop()
    
