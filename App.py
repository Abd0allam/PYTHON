import re
import datetime

class Authentication:
    def __init__(self):
        self.users_file = "users.txt"
        self.projects_file = "projects.txt"
        self.logged_in_user = None

    def validate_names(self, f_name, l_name):
        pattern = r"^[a-zA-Z]+$"  
        return bool(re.match(pattern, f_name)) and bool(re.match(pattern, l_name))

    def validate_email(self, email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))    

    def validate_phone_number(self, phone_number):
        pattern = r"01[0125][0-9]{8}"
        return bool(re.match(pattern, phone_number))
    
    def validate_password(self, password):
        pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        return bool(re.match(pattern, password))

    def sign_up(self):
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        confirm_password = input("Confirm your password: ")
        mobile = input("Enter your mobile phone number: ")


        while not self.validate_names(first_name, last_name):
            print("Invalid name(s). Enter only alphabetic characters.")
            first_name = input("Enter your first name: ")
            last_name = input("Enter your last name: ")

        while not self.validate_email(email):
            print("Invalid email address.")
            email = input("Enter your email: ")

        while not self.validate_phone_number(mobile):
            mobile = input("Invalid phone number. Enter a valid phone number (11 digits): ")

        while not self.validate_password(password):
            print("Invalid password. Password must be at least 8 characters long and contain at least one special character.")
            password = input("Enter your password: ")
            confirm_password = input("Confirm your password: ")

            
        if password != confirm_password :
            print("Passwords do not match.")
            self.sign_up()
        else:
            with open(self.users_file, "a") as f:
                f.write(f"{first_name},{last_name},{email},{password},{mobile}\n")
                print("Sign up successful.")
    
    def log_in(self):
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        with open(self.users_file, "r") as f:
            for line in f.readlines():
                user_info = line.strip().split(",")
                if user_info[2] == email and user_info[3] == password:
                    self.logged_in_user = user_info
                    print(f"Hello {user_info[0]}!")
                    return

        answer = input("User not found. Do you want to sign up? (y/n) ")
        if answer.lower() == "y":
            self.sign_up()
        else:
            print("Goodbye.")

    def create_project(self):
        title = input("Enter project title: ")
        details = input("Enter project details: ")
        total_target = input("Enter total target amount (in EGP): ")
        start_time_str = input("Enter start time (in the format of yyyy-mm-dd): ")
        start_time = self.get_valid_date(start_time_str)
        end_time_str = input("Enter end time (in the format of yyyy-mm-dd): ")
        end_time = self.get_valid_date(end_time_str)
        with open(self.projects_file, "a") as f:
            f.write(f"{self.logged_in_user[2]},{title},{details},{total_target},{start_time},{end_time}\n")
            # self.logged_in_user[2]==>email
            print("Project created successfully.")

        
    def view_projects(self):
        with open(self.projects_file, "r") as f:
            for line in f.readlines():
                project_info = line.strip().split(",")
                print(f"Title: {project_info[1]}")
                print(f"Details: {project_info[2]}")
                print(f"Total target: {project_info[3]} EGP")
                print(f"Start time: {project_info[4]}")
                print(f"End time: {project_info[5]}\n")

    def edit_project(self):
        title_to_edit = input("Enter project title to edit: ")
        with open(self.projects_file, "r+") as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                project_info = line.strip().split(",")
                if project_info[0] == self.logged_in_user[2] and project_info[1] == title_to_edit:
                    new_title = input("Enter new project title: ")
                    new_details = input("Enter new project details: ")
                    new_total_target = input("Enter new total target amount (in EGP): ")
                    new_start_time_str = input("Enter new start time (in the format of yyyy-mm-dd): ")
                    new_start_time = self.get_valid_date(new_start_time_str)
                    new_end_time_str = input("Enter new end time (in the format of yyyy-mm-dd): ")
                    new_end_time = self.get_valid_date(new_end_time_str)
                    line = f"{self.logged_in_user[2]},{new_title},{new_details},{new_total_target},{new_start_time},{new_end_time}\n"
                    print("Project edited successfully.")
                f.write(line)

    def delete_project(self):
        title_to_delete = input("Enter project title to delete: ")
        with open(self.projects_file, "r+") as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                project_info = line.strip().split(",")
                if project_info[0] == self.logged_in_user[2] and project_info[1] == title_to_delete:
                    continue
                f.write(line)

        print("Project deleted successfully.")
        
    def search_project_by_date(self):
        date_str = input("Enter date to search (in the format of yyyy-mm-dd): ")
        search_date = self.get_valid_date(date_str)
        with open(self.projects_file, "r") as f:
            for line in f.readlines():
                project_info = line.strip().split(",")
                start_time = datetime.datetime.strptime(project_info[4], '%Y-%m-%d')
                end_time = datetime.datetime.strptime(project_info[5], '%Y-%m-%d')
                if start_time <= search_date <= end_time:
                    print(f"Title: {project_info[1]}")
                    print(f"Details: {project_info[2]}")
                    print(f"Total target: {project_info[3]} EGP")
                    print(f"Start time: {project_info[4]}")
                    print(f"End time: {project_info[5]}\n")

    def get_valid_date(self, date_str):
        while True:
            try:
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
                return date
            except ValueError:
                print("Invalid date format. Please enter in the format of yyyy-mm-dd")
                date_str = input("Enter date to search (in the format of yyyy-mm-dd): ")

    def signing(self):
        answer = input("Do you want to sign up or log in? ")
        if answer.lower() == "sign up":
            self.sign_up()
        elif answer.lower() == "log in":
            self.log_in()
            if self.logged_in_user is not None:
                while True:
                    action = input("Do you want to create/view/edit/delete/search for a project or log out? ")
                    if action.lower() == "create":
                        self.create_project()
                    elif action.lower() == "view":
                        self.view_projects()
                    elif action.lower() == "edit":
                        self.edit_project()
                    elif action.lower() == "delete":
                        self.delete_project()
                    elif action.lower() == "search":
                        self.search_project_by_date()
                    elif action.lower() == "log out":
                        print("Goodbye.")
                        break
                    else:
                        print("Invalid action.")
        else:
            print("Invalid answer.")


Authentication().signing()