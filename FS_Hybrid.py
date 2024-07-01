
# -> * File State Application * <-

# -> Runs on Python 3.10
# -> The GUI must be installed, use the following in command prompt:
# -> pip install customtkinter



# *> TO DO LIST: <*

#  -- Local File Side --

# > 1 - Set file selection to disabled by default
# > 2 - Change folder selection to no longer show, by modifiying the functions

#  -- Cloud File Side --

# > 1 - Create interface/GUI
# > 2 - Configure AWS S3 storage and gateway API
# > 3 - Test API, determine functionality
# > 4 - Code connections between Python app and API
# > 5 - Test file read/write with the API
# > 5 - Test file navigation with the API
# > 6 - Create button for moving up the file tree
# > 7 - Create button for moving into a folder



# <*> Key Elements <*>

# -> Imports
import re
import customtkinter
import os
import csv


# <*> Selection Main <*>

class select_page(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x350")

        # -> Main select page frame
        self.select_frame = customtkinter.CTkFrame(self)
        self.select_frame.pack(pady = (20, 20), padx = (60, 60), fill = "both", expand = True)

        # -> Main label header
        self.selectHeader_Label = customtkinter.CTkLabel(self.select_frame, text = "File State", font = ("Carlito", 24))
        self.selectHeader_Label.pack(pady = (50, 20), padx = (60, 60))

        # -> Button for launching Local Saves feature
        self.localSelect_button = customtkinter.CTkButton(self.select_frame, text = "Local Files", command = self.open_localSave)
        self.localSelect_button.pack(pady = 10, padx = 10)

        # -> Button for launching Cloud Saves feature
        self.cloudSelect_button = customtkinter.CTkButton(self.select_frame, text = "Cloud Files", command = self.open_cloudSave)
        self.cloudSelect_button.pack(pady = 10, padx = 10)

        self.localSave_window = None
        self.cloudSave_window = None

    # ->
    def open_localSave(self):
        if self.localSave_window is None or not self.localSave_window.winfo_exists():
            localStart = local_page(self) # create window if its None or destroyed
            localStart.startup()
        else:
            self.localSave_window.focus()  # if window exists focus it

    def open_cloudSave(self):
        if self.cloudSave_window is None or not self.cloudSave_window.winfo_exists():
            self.cloudSave_window = cloud_page(self)  # create window if its None or destroyed
        else:
            self.cloudSave_window.focus()  # if window exists focus it


# <*> Local Saves GUI Page <*>

class local_page(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1000x650")

        # -> Master frame, ties in other elements
        self.local_frame = customtkinter.CTkFrame(self)
        self.local_frame.pack(pady = (20, 20), padx = (60, 60), fill = "both", expand = True)

        # -> Main label header
        self.localHeader_Label = customtkinter.CTkLabel(self.local_frame, text = "File State - Local Saves", font = ("Carlito", 24))
        self.localHeader_Label.pack(pady = (10, 10), padx = (10, 10))

        # -> File selection tabs
        self.tab_view = customtkinter.CTkTabview(self.local_frame, width = 100, height = 5, command = self.show_tab)
        self.tab_view.pack(pady = (2, 1), padx = (10, 10))

        # -> Button for user back out navigation
        self.tab_navigation = customtkinter.CTkButton(self.local_frame, text = "Back", command = self.backNavi_tab)
        self.tab_navigation.pack(pady = (1, 2), padx = (10, 10))

        # -> Button for user open folder navigation
        self.tab_navigation = customtkinter.CTkButton(self.local_frame, text = "Open Folder", command = self.openNavi_tab)
        self.tab_navigation.pack(pady = (1, 2), padx = (10, 10))

        # -> Space for user email entry
        self.entry_Email = customtkinter.CTkEntry(self.local_frame, placeholder_text = "Email")
        self.entry_Email.pack(pady = (10, 10), padx = (10, 10))

        # -> Space for selecting your access mode
        self.entry_AccessMode = customtkinter.CTkEntry(self.local_frame, placeholder_text = "Access Mode")
        self.entry_AccessMode.pack(pady = (2, 2), padx = (10, 10))

        # -> Displays access mode options
        self.AccessMode_Label = customtkinter.CTkLabel(self.local_frame, text = '(Append = "a", Read = "r", Overwrite = "w")', font = ("Carlito", 14))
        self.AccessMode_Label.pack(pady = (6, 6), padx = (10, 10))

        # -> Space for entering in your text
        self.entry_UserText = customtkinter.CTkTextbox(self.local_frame, height = 200 , width = 800)
        self.entry_UserText.pack(pady = (2, 2), padx = (10, 10))

        # -> Button for user accept interaction
        self.button_accept = customtkinter.CTkButton(self.local_frame, text = "Accept", command = self.accept_Button)
        self.button_accept.pack(pady = (10, 10), padx = (10, 10))

        # -> Label to display text to user
        self.reader_Label = customtkinter.CTkLabel(self.local_frame, text = "", font = ("Carlito", 24))
        self.reader_Label.pack(pady = (6, 6), padx = (10, 10))


        # <*> GUI Triggers  <*>

        # -> Accept Button Trigger Label
        self.action_flagLabel = customtkinter.CTkLabel(self.local_frame, text = "", font = ("Carlito", 12))
        self.action_flagLabel.pack(pady = 1, padx = 1)

        # -> File Selection Button Trigger Label
        self.file_flagLabel = customtkinter.CTkLabel(self.local_frame, text = "", font = ("Carlito", 10))
        self.file_flagLabel.pack(pady = 1, padx = 1)

        # -> Folder Selection Button Trigger Label
        self.directory_flagLabel = customtkinter.CTkLabel(self.local_frame, text = "", font = ("Carlito", 10))
        self.directory_flagLabel.pack(pady = 1, padx = 1)


    # <*> Functions <*>

    # -> Function after user clicks accept
    def accept_Button(self):
    

        # -> Regular expression to check against user email
        emailPattern = re.compile("^[a-zA-Z0-9]+[^a-zA-Z0-9]{1}[a-zA-Z]+[^a-zA-Z0-9]{1}[a-z]{3}$")

        # -> Declares Variables
        label_State = self.action_flagLabel.cget("text")
        user_Email = ""
        user_Text = ""
        typeState = False
        emailState = False

        # -> Checks the state of a label, to verify user clicked button, which kick starts everything else
        if label_State == "":
            self.action_flagLabel.configure(text = "Success!")
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
            filename = passedValue.cget("text")
            path = os.getcwd()
            retreivedValue = os.path.join(path, filename)
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
                    self.reader_Label.configure(text = "Success!")
                
                # -> Reads from file
                elif typeState == False and emailState == True:
                    self.entry_UserText.delete("0.0", "end")
                    for steps in dataFile:
                        self.entry_UserText.insert("0.0", steps)

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

                user_Email = retreiver(self.entry_Email).lower()
                User_File = file_retreiver(self.file_flagLabel)
                testedEmail = emailChecker(user_Email)

                if testedEmail != None:
                    emailState = True
                    break

                elif testedEmail == None: 
                    self.reader_Label.configure(text = "Please enter a valid email")
                    print("Please enter a valid email")

            # -> Request user data
            user_AccessMode = retreiver(self.entry_AccessMode).lower()

            # -> Checks if the user will be writing to the file
            if user_AccessMode == "w" or user_AccessMode == "w+" or user_AccessMode == "a":
                typeState = True
            if typeState == True:
                user_Text = textmonkey(self.entry_UserText)


            # -> Error handling for Sanitization function
            try:
                cleanUser_Email = sanitized(user_Email)
                cleanUser_AccessMode = sanitized(user_AccessMode)
                cleanUser_Text = sanitized(user_Text)
            except:
                # -> Clean input failed
                self.reader_Label.configure(text = " \nError C050: bad input\n ")
                print(" \nError C050: bad input\n ")

            # -> Error handling for openFile function
            try:
                # -> Passing user input into open file function
                openFile(User_File, cleanUser_AccessMode, cleanUser_Text, cleanUser_Email)
            except:
                # -> Failed to send user input to file function or file not found
                self.reader_Label.configure(text = " \nError F040: file failure\n ")
                print(" \nError F040: file failure\n ")
                
            if label_State == "Success!":
                self.action_flagLabel.configure(text = "") 

        return

    # -> Function to Display the found files/folders as tabs
    def show_tab(self):
        stages = self.tab_view.get()
        self.file_flagLabel.configure(text = stages)

    # -> Function to back out of file folders
    def backNavi_tab(self):

        # -> Checks current directory and objects within
        director = os.listdir()
        dataFromFile = csv.reader(director, delimiter = ",")
            
        # -> Displays folders and files
        for pointz in dataFromFile:
            comeTogether = "".join(pointz)
            self.tab_view.delete(comeTogether)

        try:
            os.chdir('..')
            self.reader_Label.configure(text = "Success!")
        except:
            self.reader_Label.configure(text = "Error, Could not change directory.")

            # -> Kick Starts the tab labels, checking current files/folders
        try:
            self.show_FileFolders()
        except:
            self.reader_Label.configure(text = "Error, Could not show files")

    # -> Function to open file folders
    def openNavi_tab(self):

        # -> Locates the current file path
        fileName = (self.file_flagLabel.cget("text"))

        # -> Checks current directory and objects within
        director = os.listdir()
        dataFromFile = csv.reader(director, delimiter = ",")
            
        # -> Removes Displayed folders and files
        for pointz in dataFromFile:
            comeTogether = "".join(pointz)
            self.tab_view.delete(comeTogether)

        # -> Simply combines text to "show" as a proper file path
        try:
            os.chdir(fileName)
            self.reader_Label.configure(text = "Success!")
        except:
            self.reader_Label.configure(text = "Invalid Folder, Please select a folder.")

            # -> Kick Starts the tab labels, checking current files/folders
        try:
            self.show_FileFolders()
        except:
            self.reader_Label.configure(text = "Error, Could not show files")

    # -> Function to get the current directory files/folders
    def show_FileFolders(self):
        # -> Checks current directory and objects within
        director = os.listdir()
        dataFromFile = csv.reader(director, delimiter = ",")
            
        # -> Displays folders and files
        for pointz in dataFromFile:
            comeTogether = "".join(pointz)
            self.tab_view.add(comeTogether)

    
    # <*> Starting Elements <*>

    def startup(self):
        # -> Inserting fake text in textbox
        self.entry_UserText.insert("0.0", "Enter Text Here")

        # -> Kick Starts the tab labels, checking current files/folders
        try:
            self.show_FileFolders()
        except:
            print("Error could not show files")


# <*> Cloud Saves GUI Page <*>

class cloud_page(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("800x550")

        # -> Master frame, ties in other elements
        self.cloud_frame = customtkinter.CTkFrame(self)
        self.cloud_frame.pack(pady = (20, 20), padx = (60, 60), fill = "both", expand = True)

        # -> Main label header
        self.cloudHeader_Label = customtkinter.CTkLabel(self.cloud_frame, text = "File State - Cloud Saves", font = ("Carlito", 24))
        self.cloudHeader_Label.pack(pady = (10, 10), padx = (10, 10))


selectPage = select_page()
selectPage.mainloop()
