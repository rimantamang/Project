import json
import os
if os.path.exists("student_info.json"):
    with open("student_info.json", "r") as f:
        try:
            stud_info = json.load(f)
        except json.JSONDecodeError:
            stud_info = {}
else:
    stud_info = {}
print("Welcome to the Student Management System!")
print("--- Student Management System---")
Username = input("Username: ")
Password = input("Password: ")

if Username=="admin" and Password=="admin123":
    print("Login Successful! Role:Admin")
    print("1.Add Student")
    print("2.Delete Student")
    print("3.Update Marks")
    print("4.View Students")
    print("5.Search Students")
    print("6.Sort Students")
    print("7.View Topper")
    print("8.Export to CSV")
    print("0.Exit")
    a= input("\nSelect:")
    if a=='1':
        while True:
            roll_no = input("Enter Roll No: ")
            name = input("Enter Student Name: ")
            marks = int(input("Enter Marks: "))
            if marks>=90:
                grade="A"
            elif marks>=75:
                grade="B"
            elif marks>= 60:
                grade="C"
            elif marks>=40:
                grade="D"
            elif marks<40:
                grade="F"
            stud_info[roll_no]={
            "Roll no":roll_no,
            "Name":name,
            "Marks":marks,
            "Grade":grade
            }
            print(f"Student Info for {roll_no} has been added.")
            print(stud_info) 
            with open("student_info.json", "w") as f:
                json.dump(stud_info, f, indent=4)
            Ia=input("Do you want to add another student info? (y/n)?")
            if Ia=="n":
                break
    elif a=='4':
        with open("student_info.json","r") as f:
            data=json.load(f)
            print(json.dumps(data, indent=4))
                
elif Username=="user" and Password=="user123":
    print("1.View Students")
    print("2.Search Student")
    print("3.View Topper")
    print("4.Sort Students")
    print("0.Exit")
    u= input("Select:")
    if u=='1':
        with open("student_info.json","r") as f:
            data=json.load(f)
            print(json.dumps(data, indent=4))
else:
    print("Invalid Credentials")
