#------------------------------------------------------------------------------------#
# -> * File State Application * <-
#------------------------------------------------------------------------------------#

# -> Runs on Python 3.10
# -> The libraries must be installed before editing, use the following in command prompt or terminal:

# -> pip install regex
# -> pip install customtkinter
# -> pip install os
# -> pip install csv
# -> pip install requests


#------------------------------------------------------------------------------------#
# { A1 } *> TO DO LIST: <*
#------------------------------------------------------------------------------------#

#  -- Cloud File Side --

# > 1 - Create interface/GUI
# > 2 - Configure AWS S3 storage and gateway API
# > 3 - Test API, determine functionality
# > 4 - Code connections between Python app and API
# > 5 - Test file read/write with the API
# > 5 - Test file navigation with the API
# > 6 - Create button for moving up the file tree
# > 7 - Create button for moving into a folder

#  -- Local File Side --

# > 1 - Change folder selection to no longer show, by modifiying the functions


#------------------------------------------------------------------------------------#
# { B1 } <*> Key Elements <*>
#------------------------------------------------------------------------------------#

# -> Imports
import re
import customtkinter
import os
import csv
import requests


#------------------------------------------------------------------------------------#
# { C1 } <*> Selection Main <*>
#------------------------------------------------------------------------------------#

class select_page(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x350")

        # -> Main select page frame
        self.select_frame = customtkinter.CTkFrame(self)
        self.select_frame.pack(pady = (20, 20), padx = (60, 60), fill = "both", expand = True)

        # -> Main label header
        self.select_header_label = customtkinter.CTkLabel(self.select_frame, text = "File State", font = ("Carlito", 24))
        self.select_header_label.pack(pady = (50, 20), padx = (60, 60))

        # -> Button for launching Local Saves feature
        self.local_select_button = customtkinter.CTkButton(self.select_frame, text = "Local Files", command = self.open_local_save)
        self.local_select_button.pack(pady = 10, padx = 10)

        # -> Button for launching Cloud Saves feature
        self.cloud_select_button = customtkinter.CTkButton(self.select_frame, text = "Cloud Files", command = self.open_cloud_save)
        self.cloud_select_button.pack(pady = 10, padx = 10)

        self.local_save_window = None
        self.cloud_save_window = None

    # ->
    def open_local_save(self):
        if self.local_save_window is None or not self.local_save_window.winfo_exists():
            local_start = local_page(self) # create window if its None or destroyed
            local_start.startup()
        else:
            self.local_save_window.focus()  # if window exists focus it

    def open_cloud_save(self):
        if self.cloud_save_window is None or not self.cloud_save_window.winfo_exists():
            self.cloud_save_window = cloud_page(self)  # create window if its None or destroyed
        else:
            self.cloud_save_window.focus()  # if window exists focus it


#------------------------------------------------------------------------------------#
# { D1 } <*> Local Saves GUI Page <*>
#------------------------------------------------------------------------------------#

class local_page(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1000x650")

        # -> Master frame, ties in other elements
        self.local_frame = customtkinter.CTkFrame(self)
        self.local_frame.pack(pady = (20, 20), padx = (60, 60), fill = "both", expand = True)

        # -> Main label header
        self.local_header_label = customtkinter.CTkLabel(self.local_frame, text = "File State - Local Saves", font = ("Carlito", 24))
        self.local_header_label.pack(pady = (10, 10), padx = (10, 10))

        # -> File selection tabs
        self.tab_view = customtkinter.CTkTabview(self.local_frame, width = 100, height = 5, command = self.show_tab)
        self.tab_view.pack(pady = (2, 1), padx = (10, 10))

        # -> Button for user back out navigation
        self.localtab_navigation = customtkinter.CTkButton(self.local_frame, text = "Back", command = self.back_navi_tab)
        self.localtab_navigation.pack(pady = (1, 2), padx = (10, 10))

        # -> Button for user open folder navigation
        self.tab_navigation = customtkinter.CTkButton(self.local_frame, text = "Open Folder", command = self.open_navi_tab)
        self.tab_navigation.pack(pady = (1, 2), padx = (10, 10))

        # -> Space for user email entry
        self.entry_email = customtkinter.CTkEntry(self.local_frame, placeholder_text = "Email")
        self.entry_email.pack(pady = (10, 10), padx = (10, 10))

        # -> Space for selecting your access mode
        self.entry_access_mode = customtkinter.CTkEntry(self.local_frame, placeholder_text = "Access Mode")
        self.entry_access_mode.pack(pady = (2, 2), padx = (10, 10))

        # -> Displays access mode options
        self.access_mode_label = customtkinter.CTkLabel(self.local_frame, text = '(Append = "a", Read = "r", Overwrite = "w")', font = ("Carlito", 14))
        self.access_mode_label.pack(pady = (6, 6), padx = (10, 10))

        # -> Space for entering in your text
        self.entry_user_text = customtkinter.CTkTextbox(self.local_frame, height = 200 , width = 800)
        self.entry_user_text.pack(pady = (2, 2), padx = (10, 10))

        # -> Button for user accept interaction
        self.button_accept = customtkinter.CTkButton(self.local_frame, text = "Accept", command = self.accept_button)
        self.button_accept.pack(pady = (10, 10), padx = (10, 10))

        # -> Label to display text to user
        self.reader_label = customtkinter.CTkLabel(self.local_frame, text = "", font = ("Carlito", 24))
        self.reader_label.pack(pady = (6, 6), padx = (10, 10))


#------------------------------------------------------------------------------------#
        # { E1 } <*> GUI Triggers  <*>
#------------------------------------------------------------------------------------#

        # -> Accept Button Trigger Label
        self.action_flag_label = customtkinter.CTkLabel(self.local_frame, text = "", font = ("Carlito", 12))
        self.action_flag_label.pack(pady = 1, padx = 1)

        # -> File Selection Button Trigger Label
        self.file_flag_label = customtkinter.CTkLabel(self.local_frame, text = "", font = ("Carlito", 10))
        self.file_flag_label.pack(pady = 1, padx = 1)

        # -> Folder Selection Button Trigger Label
        self.directory_flag_label = customtkinter.CTkLabel(self.local_frame, text = "", font = ("Carlito", 10))
        self.directory_flag_label.pack(pady = 1, padx = 1)


#------------------------------------------------------------------------------------#
    # { F1 } <*> Local Functions <*>
#------------------------------------------------------------------------------------#

    # -> Function after user clicks accept
    def accept_button(self):
    

        # -> Regular expression to check against user email
        email_pattern = re.compile("^[a-zA-Z0-9]+[^a-zA-Z0-9]{1}[a-zA-Z]+[^a-zA-Z0-9]{1}[a-z]{3}$")

        # -> Declare Variables
        label_state = self.action_flag_label.cget("text")
        user_email = ""
        user_text = ""
        type_state = False
        email_state = False

        # -> Checks the state of a label, to verify user clicked button, which kick starts everything else
        if label_state == "":
            self.action_flag_label.configure(text = "Success!")
            label_state = "Success!"

        # -> Function to retreive user text values
        def text_monkey(passed_value):
            retreived_value = passed_value.get("0.0", "end")
            return retreived_value

        # -> Function to retreive user entered values
        def retreiver(passed_value):
            retreived_value = passed_value.get()
            return retreived_value
        
        # -> Function to retreive file/folder name
        def file_retreiver(passed_value):
            file_name = passed_value.cget("text")
            path = os.getcwd()
            retreived_value = os.path.join(path, file_name)
            return retreived_value

        # -> Function to sanitize user input
        def sanitized(user_input):
            cleaned_input = user_input.replace("?","0.A.0.Z.1.A").replace("&","0.A.1.A.1.A").replace("%","0.A.2.B.1.A").replace("*","0.A.3.C.1.A").replace("(","0.A.4.D.1.A").replace(")","0.A.5.E.1.A").replace("{","0.A.6.F.1.A").replace("}","0.A.7.G.1.A").replace("]","0.A.8.H.1.A").replace("[","0.A.9.I.1.A").replace(",","1.A.0.J.1.A").replace("<","1.A.1.K.1.A").replace(">","1.A.2.L.1.A").replace("!","1.A.3.M.1.A").replace("/","1.A.4.N.1.A").replace("\\","1.A.5.O.1.A").replace("|","1.A.6.P.1.A").replace("=","1.A.7.Q.1.A").replace("#","1.A.8.R.1.A").replace("^","1.A.9.S.1.A").replace("$","2.A.0.T.1.A").replace("@","2.A.1.U.1.A")
            return cleaned_input

        # -> Function to check user entered a valid email
        def email_checker(user_email):
            email_test = email_pattern.match(user_email)
            if email_test != None:
                print("Vaild Email")

            return email_test

        # -> Import function, set to read from file
        def open_file(file_opener, access_mode, user_input, user_email):
            with open(file_opener, access_mode) as data_file:

                # -> Writes to file
                if type_state == True and email_state == True:
                    final_user_email = user_email.replace("2.A.1.U.1.A", "@")
                    final_user_input = user_input.replace("0.A.0.Z.1.A","?").replace("0.A.1.A.1.A","&").replace("0.A.2.B.1.A","%").replace("0.A.3.C.1.A","*").replace("0.A.4.D.1.A","(").replace("0.A.5.E.1.A",")").replace("0.A.6.F.1.A","{").replace("0.A.7.G.1.A","}").replace("0.A.8.H.1.A","]").replace("0.A.9.I.1.A","[").replace("1.A.0.J.1.A",",").replace("1.A.1.K.1.A","<").replace("1.A.2.L.1.A",">").replace("1.A.3.M.1.A","!").replace("1.A.4.N.1.A","/").replace("1.A.5.O.1.A","\\").replace("1.A.6.P.1.A","|").replace("1.A.7.Q.1.A","=").replace("1.A.8.R.1.A","#").replace("1.A.9.S.1.A","^").replace("2.A.0.T.1.A","$").replace("2.A.1.U.1.A", "@")
                    data_file.write("\n " + final_user_email + " - " + final_user_input)
                    self.reader_label.configure(text = "Success!")
                
                # -> Reads from file
                elif type_state == False and email_state == True:
                    self.entry_user_text.delete("0.0", "end")
                    for steps in data_file:
                        self.entry_user_text.insert("0.0", steps)

                return data_file


#------------------------------------------------------------------------------------#
        # { G1 } <*> User Input <*>
#------------------------------------------------------------------------------------#

        # -> Kick Start for the app
        for loop_element in range(1):
                
            # -> Loop to check for a valid email
            for email_loop in range(1):

                user_email = retreiver(self.entry_email).lower()
                user_file = file_retreiver(self.file_flag_label)
                tested_email = email_checker(user_email)

                if tested_email != None:
                    email_state = True
                    break

                elif tested_email == None: 
                    self.reader_label.configure(text = "Error G01: Please enter a valid email")
                    
            # -> Request user data
            user_access_mode = retreiver(self.entry_access_mode).lower()

            # -> Checks if the user will be writing to the file
            if user_access_mode == "w" or user_access_mode == "w+" or user_access_mode == "a":
                type_state = True
            if type_state == True:
                user_text = text_monkey(self.entry_user_text)


            # -> Error handling for Sanitization function
            try:
                clean_user_email = sanitized(user_email)
                clean_user_access_mode = sanitized(user_access_mode)
                clean_user_text = sanitized(user_text)
            except:
                # -> Clean input failed
                self.reader_label.configure(text = " \nError G02: bad input\n ")
                
            # -> Error handling for open_file function
            try:
                # -> Passing user input into open file function
                open_file(user_file, clean_user_access_mode, clean_user_text, clean_user_email)
            except:
                # -> Failed to send user input to file function or file not found
                self.reader_label.configure(text = " \nError G03: file failure\n ")
                                
            if label_state == "Success!":
                self.action_flag_label.configure(text = "") 

        return

    # -> Function to Display the found files/folders as tabs
    def show_tab(self):
        stages = self.tab_view.get()
        self.file_flag_label.configure(text = stages)

    # -> Function to back out of file folders
    def back_navi_tab(self):

        # -> Checks current directory and objects within
        director = os.listdir()
        data_from_file = csv.reader(director, delimiter = ",")
            
        # -> Displays folders and files
        for pointz in data_from_file:
            come_together = "".join(pointz)
            self.tab_view.delete(come_together)

        try:
            os.chdir('..')
            self.reader_label.configure(text = "Success!")
        except:
            self.reader_label.configure(text = "Error G04: Could not change directory.")

            # -> Kick Starts the tab labels, checking current files/folders
        try:
            self.show_file_folders()
        except:
            self.reader_label.configure(text = "Error G05: Could not show files")

    # -> Function to open file folders
    def open_navi_tab(self):

        # -> Locates the current file path
        file_name = (self.file_flag_label.cget("text"))

        # -> Checks current directory and objects within
        director = os.listdir()
        data_from_file = csv.reader(director, delimiter = ",")
            
        # -> Removes Displayed folders and files
        for pointz in data_from_file:
            come_together = "".join(pointz)
            self.tab_view.delete(come_together)

        # -> Simply combines text to "show" as a proper file path
        try:
            os.chdir(file_name)
            self.reader_label.configure(text = "Success!")
        except:
            self.reader_label.configure(text = "Error G06: Invalid Folder")

            # -> Kick Starts the tab labels, checking current files/folders
        try:
            self.show_file_folders()
        except:
            self.reader_label.configure(text = "Error G07: Could not show files")

    # -> Function to get the current directory files/folders
    def show_file_folders(self):
        # -> Checks current directory and objects within
        director = os.listdir()
        data_from_file = csv.reader(director, delimiter = ",")
            
        # -> Displays folders and files
        for pointz in data_from_file:
            come_together = "".join(pointz)
            self.tab_view.add(come_together)


#------------------------------------------------------------------------------------#    
    # { H1 } <*> Local Starting Elements <*>
#------------------------------------------------------------------------------------#

    def startup(self):
        # -> Inserting fake text in textbox
        self.entry_user_text.insert("0.0", "Enter Text Here")
        self.tab_view.add("?")

        # -> Kick Starts the tab labels, checking current files/folders
        try:
            self.show_file_folders()
        except:
            self.reader_label.configure(text = "Error H01, Could not show files")


#------------------------------------------------------------------------------------#
# { I1 } <*> Cloud Saves GUI Page <*>
#------------------------------------------------------------------------------------#

class cloud_page(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1000x650")

        # -> Master frame, ties in other elements
        self.cloud_frame = customtkinter.CTkFrame(self)
        self.cloud_frame.pack(pady = (20, 20), padx = (60, 60), fill = "both", expand = True)

        # -> Main label header
        self.cloud_header_label = customtkinter.CTkLabel(self.cloud_frame, text = "File State - Cloud Saves", font = ("Carlito", 24))
        self.cloud_header_label.pack(pady = (10, 10), padx = (10, 10))

        # -> File selection tabs
        self.cloud_tab_view = customtkinter.CTkTabview(self.cloud_frame, width = 100, height = 5, command = self.cloud_show_tab)
        self.cloud_tab_view.pack(pady = (2, 1), padx = (10, 10))

        # -> Button for user back out navigation
        self.cloud_back_navigation = customtkinter.CTkButton(self.cloud_frame, text = "Back", command = self.cloud_back_navi_tab)
        self.cloud_back_navigation.pack(pady = (1, 2), padx = (10, 10))

        # -> Button for user open folder navigation
        self.cloud_tab_navigation = customtkinter.CTkButton(self.cloud_frame, text = "Open Folder", command = self.cloud_open_navi_tab)
        self.cloud_tab_navigation.pack(pady = (1, 2), padx = (10, 10))

        # -> Space for user email entry
        self.cloud_entry_email = customtkinter.CTkEntry(self.cloud_frame, placeholder_text = "Email")
        self.cloud_entry_email.pack(pady = (10, 10), padx = (10, 10))

        # -> Space for selecting your access mode
        self.cloud_entry_access_mode = customtkinter.CTkEntry(self.cloud_frame, placeholder_text = "Access Mode")
        self.cloud_entry_access_mode.pack(pady = (2, 2), padx = (10, 10))

        # -> Displays access mode options
        self.cloud_access_mode_label = customtkinter.CTkLabel(self.cloud_frame, text = '(Append = "a", Read = "r", Overwrite = "w")', font = ("Carlito", 14))
        self.cloud_access_mode_label.pack(pady = (6, 6), padx = (10, 10))

        # -> Space for entering in your text
        self.cloud_entry_user_text = customtkinter.CTkTextbox(self.cloud_frame, height = 200 , width = 800)
        self.cloud_entry_user_text.pack(pady = (2, 2), padx = (10, 10))

        # -> Button for user accept interaction
        self.cloud_button_accept = customtkinter.CTkButton(self.cloud_frame, text = "Accept", command = self.cloud_accept_button)
        self.cloud_button_accept.pack(pady = (10, 10), padx = (10, 10))

        # -> Label to display text to user
        self.cloud_reader_label = customtkinter.CTkLabel(self.cloud_frame, text = "", font = ("Carlito", 24))
        self.cloud_reader_label.pack(pady = (6, 6), padx = (10, 10))


#------------------------------------------------------------------------------------#
        # { J1 } <*> Cloud GUI Triggers  <*>
#------------------------------------------------------------------------------------#

        # -> Accept Button Trigger Label
        self.cloud_action_flag_label = customtkinter.CTkLabel(self.cloud_frame, text = "", font = ("Carlito", 12))
        self.cloud_action_flag_label.pack(pady = 1, padx = 1)

        # -> File Selection Button Trigger Label
        self.cloud_file_flag_label = customtkinter.CTkLabel(self.cloud_frame, text = "", font = ("Carlito", 10))
        self.cloud_file_flag_label.pack(pady = 1, padx = 1)

        # -> Folder Selection Button Trigger Label
        self.cloud_directory_flag_label = customtkinter.CTkLabel(self.cloud_frame, text = "", font = ("Carlito", 10))
        self.cloud_directory_flag_label.pack(pady = 1, padx = 1)

#------------------------------------------------------------------------------------#
    # { K1 } <*> Cloud Functions <*>
#------------------------------------------------------------------------------------#

    def cloud_show_tab(self):
        print("hi")

    def cloud_back_navi_tab(self):
        print("hi")
    
    def cloud_open_navi_tab(self):
        print("hi")

    def cloud_accept_button(self):
        self.api_request()

#------------------------------------------------------------------------------------#
    # { L1 } <*> API Communications <*>
#------------------------------------------------------------------------------------#

    # -> Function to get data from the api
    def api_request(status):
        try:
            api_response = requests.get("https://randomuser.me/api")
            api_status_code = str(api_response.status_code)
            print("Status: " + api_status_code)
        except:
            print("Status: " + api_status_code)
        return api_response
    
    # -> Function to convert data from api into Json
    def reply_json(api_response):
        api_reply_json = api_response.json()
        return api_reply_json
    
    # -> Function to read Json and find data
    def api_data_reader(self):
        
        api_reply = self.api_request()
        api_json = self.reply_json(api_reply)
        return api_json

select_main_page = select_page()
select_main_page.mainloop()
