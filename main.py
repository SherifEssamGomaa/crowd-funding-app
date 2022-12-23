import datetime
import re
from getpass import getpass
import phonenumbers
from phonenumbers import carrier, timezone, geocoder
import os


def search_project():
    while True:
        print("Note: Start date should be before end date")
        while True:
            date_string = input("Please enter project search start date in format YYY-MM-DD ")
            date_format = '%Y-%m-%d'
            try:
                date_object = datetime.datetime.strptime(date_string, date_format)
                search_start_date = date_object.date()
                break
            except ValueError:
                print("ERROR::Invalid date")
        while True:
            date_string = input("Please enter project end date in format YYY-MM-DD ")
            date_format = '%Y-%m-%d'
            try:
                date_object = datetime.datetime.strptime(date_string, date_format)
                search_end_date = date_object.date()
                break
            except ValueError:
                print("ERROR::Invalid date")
        if search_start_date < search_end_date:
            break
    try:
        file_object = open("projects.txt", "r")
    except Exception as e:
        print("ERROR::No projects to search")
    else:
        for line in file_object:
            line_list = line.split(";")
            project_start_date_as_string = line_list[5]
            project_end_date_as_string = line_list[6]
            date_format = '%Y-%m-%d'
            start_date_object = datetime.datetime.strptime(project_start_date_as_string, date_format)
            project_start_date_as_date = start_date_object.date()
            date_format = '%Y-%m-%d'
            end_date_object = datetime.datetime.strptime(project_end_date_as_string, date_format)
            project_end_date_as_date = end_date_object.date()
            if search_start_date <= project_start_date_as_date and search_end_date >= project_end_date_as_date:
                print("\tID: " + line_list[0])
                print("\tTitle: " + line_list[2])
                print("\tDetails: " + line_list[3])
                print("\tTarget: " + line_list[4])
                print("\tStart date: " + line_list[5])
                print("\tEnd date: " + line_list[6])
        file_object.close()


def get_projects_ids():
    ids = []
    try:
        file_object = open("projects.txt", "r")
    except Exception as e:
        ids = []
    else:
        for line in file_object:
            ids.append(line[0])
        file_object.close()
    return ids


def get_projects_data():
    data = []
    try:
        file_object = open('projects.txt', 'r')
    except Exception as e:
        data = []   
    else:
        data = file_object.readlines()
        file_object.close()
    return data


def get_line_to_update_or_delete(project_update_or_delete_id):
    line_to_update_or_delete = 0
    try:
        file_object = open("projects.txt", "r")
    except Exception as e:
        print("ERROR::No projects to edit or delete")
    else:
        i=1
        for line in file_object:
            line_list = line.split(";")
            if line_list[0] == project_update_or_delete_id:
                line_to_update_or_delete = i
            i = i+1
        file_object.close()
    return line_to_update_or_delete


def view_user_projects(user_id):
    print("Your projects:")
    try:
        file_object = open("projects.txt", "r")
    except Exception as e:
        print("ERROR::No projects to edit or delete")
    else:
        i = 1
        for line in file_object:
            line_list = line.split(";")
            if line_list[1] == user_id:
                print("Your project " + str(i) + ":")
                print("\tID: " + line_list[0])
                print("\tTitle: " + line_list[2])
                print("\tDetails: " + line_list[3])
                print("\tTarget: " + line_list[4])
                print("\tStart date: " + line_list[5])
                print("\tEnd date: " + line_list[6])
                i = i + 1
        file_object.close()


def delete_project(activ_id):
    view_user_projects(activ_id)
    ids = get_projects_ids()
    data = get_projects_data()
    if len(data) == 0:
        print("ERROR::No projects to delete")
        return
    project_to_delete_id = input("Please enter the ID of the project you want to delete ")
    while project_to_delete_id.isdigit() == False or project_to_delete_id not in ids:
        print("ERROR::Invalid ID")
        project_to_delete_id = input("Please enter the ID of the project you want to delete ")
    line_of_project_to_delete = get_line_to_update_or_delete(project_to_delete_id)
    project_to_delete_as_string = data[line_of_project_to_delete-1]
    project_to_delete_as_list = project_to_delete_as_string.split(";")
    project_to_delete_user_id = project_to_delete_as_list[1]
    if activ_id != project_to_delete_user_id:
        print("ERROR::You don't own this project")
        return
    del data[line_of_project_to_delete-1]
    with open('projects.txt', 'w', encoding='utf-8') as file:
        file.writelines(data)
    print("Project deleted successfully")


def edit_project(activ_id):
    view_user_projects(activ_id)
    ids = get_projects_ids()
    data = get_projects_data()
    if len(data) == 0:
        print("ERROR::No projects to edit")
        return
    project_to_edit_id = input("Please enter the ID of the project you want to edit ")
    while project_to_edit_id.isdigit() == False or project_to_edit_id not in ids:
        print("ERROR::Invalid ID")
        project_to_edit_id = input("Please enter the ID of the project you want to edit ")
    line_of_project_to_edit = get_line_to_update_or_delete(project_to_edit_id)
    project_to_edit_as_string = data[line_of_project_to_edit-1]
    project_to_edit_as_list = project_to_edit_as_string.split(";")
    project_to_edit_user_id = project_to_edit_as_list[1]
    if activ_id != project_to_edit_user_id:
        print("ERROR::You don't own this project")
        return
    choice = input("Enter a number to edit 1-project title 2-project details 3-project target 4-project start and end dates ")
    while choice.isdigit() == False or int(choice) not in range(1, 5):
        print("ERROR:Invalid choice")
        choice = input("Enter a number to edit 1-project title 2-project details 3-project target 4-project start and end dates ")
    if choice == "1":
        new_title = input("Please enter project new title ")
        project_to_edit_as_list[2] = new_title
        project_to_edit_as_string = ';'.join(project_to_edit_as_list)
        data[line_of_project_to_edit-1] = project_to_edit_as_string
    if choice == "2":
        new_details = input("Please enter project new details ")
        project_to_edit_as_list[3] = new_details
        project_to_edit_as_string = ';'.join(project_to_edit_as_list)
        data[line_of_project_to_edit-1] = project_to_edit_as_string
    if choice == "3":
        new_target = input("Please enter project new target ")
        while not new_target.isdigit() or int(new_target) <= 0:
            print("ERROR::Invalid project target")
            new_target = input("Please enter project new target ")
        project_to_edit_as_list[4] = new_target
        project_to_edit_as_string = ';'.join(project_to_edit_as_list)
        data[line_of_project_to_edit-1] = project_to_edit_as_string
    if choice == "4":
        while True:
            print("Note: Start date should be before end date")
            while True:
                date_string = input("Please enter project new start date in format YYY-MM-DD ")
                date_format = '%Y-%m-%d'
                try:
                    date_object = datetime.datetime.strptime(date_string, date_format)
                    new_start_date = date_object.date()
                    break
                except ValueError:
                    print("ERROR::Invalid date")
            while True:
                date_string = input("Please enter project new end date in format YYY-MM-DD ")
                date_format = '%Y-%m-%d'
                try:
                    date_object = datetime.datetime.strptime(date_string, date_format)
                    new_end_date = date_object.date()
                    break
                except ValueError:
                    print("ERROR::Invalid date")
            if new_start_date < new_end_date:
                break
        project_to_edit_as_list[5] = str(new_start_date)
        project_to_edit_as_list[6] = str(new_end_date)
        project_to_edit_as_string = ';'.join(project_to_edit_as_list)
        data[line_of_project_to_edit-1] = project_to_edit_as_string
    with open('projects.txt', 'w', encoding='utf-8') as file:
        file.writelines(data)
    print("Project updated successfully")


def view_projects():
    try:
        file_object = open("projects.txt", "r")
    except Exception as e:
        print("ERROR::No projects to list")
    else:
        i = 1
        for line in file_object:
            line_list = line.split(";")
            print("Project " + str(i) + ":")
            print("\tID: " + line_list[0])
            print("\tTitle: " + line_list[2])
            print("\tDetails: " + line_list[3])
            print("\tTarget: " + line_list[4])
            print("\tStart date: " + line_list[5])
            print("\tEnd date: " + line_list[6])
            i = i + 1
        file_object.close()


def create_project(active_id):
    title = input("Please enter project title ")
    details = input("Please enter project details ")
    target = input("Please enter project target ")
    while not target.isdigit() or int(target) <= 0:
        print("ERROR::Invalid project target")
        target = input("Please enter project target ")
    while True:
        print("Note: Start date should be before end date")
        while True:
            date_string = input("Please enter project start date in format YYY-MM-DD ")
            date_format = '%Y-%m-%d'
            try:
                date_object = datetime.datetime.strptime(date_string, date_format)
                start_date = date_object.date()
                break
            except ValueError:
                print("ERROR::Invalid date")
        while True:
            date_string = input("Please enter project end date in format YYY-MM-DD ")
            date_format = '%Y-%m-%d'
            try:
                date_object = datetime.datetime.strptime(date_string, date_format)
                end_date = date_object.date()
                break
            except ValueError:
                print("ERROR::Invalid date")
        if start_date < end_date:
            break
    try:
        file_object = open("projects.txt", "r")
    except Exception as e:
        last_project_id = 0
    else:
        last_project_id = 0
        for line in file_object:
            line_list = line.split(";")
            last_project_id = line_list[0]
        file_object.close()
    try:
        file_object = open("projects.txt", "a")
    except Exception as e:
        print(e)
    else:
        file_object.writelines([str(int(last_project_id) + 1), ";", active_id, ";", title, ";", details, ";", target, ";", str(start_date), ";", str(end_date), ";", "\n"])
        print("Project Created Successfully")
        file_object.close()


def get_second_choice():
    user_option = input("Enter a number for 1-create project 2-view projects 3-edit project 4-delete project 5-search by date 6-log-out ")
    while user_option.isdigit() == False or int(user_option) not in range(1, 7):
        print("ERROR::Invalid choice")
        user_option = input("Enter a number for 1-create project 2-view projects 3-edit project 4-delete project 5-search by date 6-log-out ")
    return user_option


def project_control(activ_id):
    option = get_second_choice()
    while option != "6":
        if option == "1":
            create_project(activ_id)
            option = get_second_choice()
        if option == "2":
            view_projects()
            option = get_second_choice()
        if option == "3":
            edit_project(activ_id)
            option = get_second_choice()
        if option == "4":
            delete_project(activ_id)
            option = get_second_choice()
        if option == "5":
            search_project()
            option = get_second_choice()
    return


def login():
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    while True:
        email = input("Please enter your email ")
        if re.fullmatch(regex, email):
            break
        else:
            print("ERROR::Invalid email")
    password = getpass("please enter your password ")
    try:
        file_object = open("users.txt", "r")
    except Exception as e:
        print("ERROR::No users to login")
    else:
        for line in file_object:
            line_list = line.split(";")
            if email == line_list[3] and password == line_list[4]:
                active_id = line_list[0]
                project_control(active_id)
                return
        print("ERROR::Invalid email or password")
        file_object.close()


def register():
    first_name = input("Please enter your first name ")
    while not first_name.isalpha():
        print("ERROR::Invalid name")
        first_name = input("Please enter your first name ")
    last_name = input("Please enter your last name ")
    while not last_name.isalpha():
        print("ERROR::Invalid name")
        last_name = input("Please enter your last name ")
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    while True:
        email = input("Please enter your email ")
        if re.fullmatch(regex, email):
            break
        else:
            print("ERROR::Invalid email")
    password = getpass("Please enter password ")
    while len(password) < 3:
        print("ERROR:Password have to be at least 3 characters")
        password = getpass("Please enter password ")
    re_password = getpass("Please enter password again ")
    while len(password) < 3:
        print("ERROR:Password have to be at least 3 characters")
    while password != re_password:
        print("ERROR::Passwords didn't match")
        password = getpass("Please enter password ")
        re_password = getpass("Please enter password again ")
    phone_number = input("Please enter your phone number with country code ")
    my_number = phonenumbers.parse(phone_number, "GB")
    country = geocoder.description_for_number(my_number, 'en')
    while phonenumbers.is_valid_number(my_number) == False or country != "Egypt":
        print("ERROR::Invalid phone number")
        phone_number = input("Please enter your phone number with country code ")
        my_number = phonenumbers.parse(phone_number, "GB")
        country = geocoder.description_for_number(my_number, 'en')
    try:
        file_object = open("users.txt", "r")
    except Exception as e:
        last_user_id = 0
    else:
        last_user_id = 0
        for line in file_object:
            line_list = line.split(";")
            last_user_id = line_list[0]
        file_object.close()
    try:
        file_object = open("users.txt", "a")
    except Exception as e:
        print(e)
    else:
        file_object.writelines([str(int(last_user_id) + 1), ";", first_name, ";", last_name, ";", email, ";", password, ";", phone_number, "\n"])
        print("User Created Successfully")
        file_object.close()


def get_first_choice():
    user_choice = input("Enter a number for 1-register 2-log-in 3-exit ")
    while user_choice != "1" and user_choice != "2" and user_choice != "3":
        print("ERROR::Invalid choice")
        user_choice = input("Enter a number for 1-register 2-log-in 3-exit ")
    return user_choice


def funding_app():
    print("-------------------------------------------------")
    print("-       Welcome to our Crowd-Funding app        -")
    print("-                 Developed by:                 -")
    print("-          Sherif Essam Ahmed Mahmoud           -")
    print("-------------------------------------------------")
    print()
    choice = get_first_choice()
    while choice != "3":
        if choice == "1":
            register()
            choice = get_first_choice()
        if choice == "2":
            login()
            choice = get_first_choice()
    print()
    print("-------------------------------------------------")
    print("-    Thanks for using our Crowd-Funding app     -")
    print("-                                               -")
    print("-                   GOOD BYE                    -")
    print("-------------------------------------------------")
    return


funding_app()
