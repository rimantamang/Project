import json
import os
import csv
#this is to check if there is any info inside the student_info json file.
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
    while True:
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
        #For adding student
        if a=='1':
            while True:
                roll_no = input("Enter Roll No: ")
                if roll_no in stud_info:
                    print(f"Error: Roll No {roll_no} already exists for {stud_info[roll_no]['Name']}.")
                    choice = input("Do you want to overwrite this record? (y/n): ").lower()
                    if choice != 'y':
                        continue
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
                else:
                    print("Invalid Marks")
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
        #for deleting student info       
        elif a == '2':
            roll_to_del = input("Enter Roll No to delete: ")
            if roll_to_del in stud_info:
                del stud_info[roll_to_del]
                with open("student_info.json", "w") as f:
                    json.dump(stud_info, f, indent=4)
                print(f"Roll No {roll_to_del} deleted successfully.")
            else:
                print("Roll No not found.")  
        #updating Marks     
        elif a == '3':
            roll_to_update = input("Enter Roll No to update marks: ")
            
            if roll_to_update in stud_info:
                # Show current info so the admin knows who they are editing
                current_student = stud_info[roll_to_update]
                print(f"Current info: {current_student['Name']} | Marks: {current_student['Marks']}")
                
                try:
                    new_marks = int(input("Enter New Marks: "))
                    
                    # 1. Update the marks in the dictionary
                    stud_info[roll_to_update]['Marks'] = new_marks
                    
                    # 2. Re-calculate the Grade automatically
                    if new_marks >= 90: 
                        new_grade = "A"
                    elif new_marks >= 75: 
                        new_grade = "B"
                    elif new_marks >= 60: 
                        new_grade = "C"
                    elif new_marks >= 40: 
                        new_grade = "D"
                    else: 
                        new_grade = "F"
                    
                    stud_info[roll_to_update]['Grade'] = new_grade
                    
                    # 3. Save the updated dictionary back to the JSON file
                    with open("student_info.json", "w") as f:
                        json.dump(stud_info, f, indent=4)
                    
                    print(f"Marks updated successfully! New Grade: {new_grade}")
                
                except ValueError:
                    print("Invalid input! Please enter a number for marks.")
            else:
                print("Error: Roll No not found.")    
        #view students    
        elif a=='4':
            with open("student_info.json","r") as f:
                data=json.load(f)
                print(json.dumps(data, indent=4))
        elif a == '5':
            search_roll = input("Enter Roll No to search: ")
            
            # Check if the roll number exists in our dictionary
            if search_roll in stud_info:
                print("\n--- Student Found ---")
                # Pull the specific student's dictionary and print it nicely
                student_data = stud_info[search_roll]
                print(json.dumps(student_data, indent=4))
            else:
                print(f"Error: No record found for Roll No {search_roll}.")        
        elif a == '6':
            if not stud_info:
                print("No students to sort.")
            else:
                # Sort by converting the Roll No (key) to an integer
                # This ensures '2' comes before '10'
                sorted_tuples = sorted(stud_info.items(), key=lambda x: int(x[0]))
                
                # Convert back to a dictionary to display nicely
                sorted_stud_info = dict(sorted_tuples)
                
                print("\n--- Students Sorted by Roll No ---")
                print(json.dumps(sorted_stud_info, indent=4))
                
                # Optional: Save this sorted order permanently to the file
                save_choice = input("Save this sorted order to file? (y/n): ").lower()
                if save_choice == 'y':
                    with open("student_info.json", "w") as f:
                        json.dump(sorted_stud_info, f, indent=4)
                    print("File updated with sorted records.")  
        elif a == '7': 
            if not stud_info:
                print("No student data available.")
            else:
                # 1. Get all unique marks and sort them highest to lowest
                all_marks = sorted(set(info['Marks'] for info in stud_info.values()), reverse=True)
                
                # 2. Loop through the top 3 scores
                ranks = ["1st (Topper)", "2nd", "3rd"]
                
                print("\n" + "="*40)
                print("       🏆 TOP 3 RANK HOLDERS 🏆       ")
                print("="*40)

                # We loop through the top 3 scores (or fewer if there aren't many students)
                for i in range(min(3, len(all_marks))):
                    target_score = all_marks[i]
                    
                    # Find all students who have this specific score
                    winners = {roll: info for roll, info in stud_info.items() if info['Marks'] == target_score}
                    
                    print(f"\n--- {ranks[i]} Place | Score: {target_score} ---")
                    print(json.dumps(winners, indent=4))
                
                print("="*40)   
        elif a == '8':
            if not stud_info:
                print("No data to export.")
            else:
                filename = "student_records.csv"
                # Define the headers (columns)
                fields = ["Roll no", "Name", "Marks", "Grade"]
            
                with open(filename, "w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=fields)
                
                    # Write the header row
                    writer.writeheader()
                
                    # Write all student data rows
                    for roll in stud_info:
                        writer.writerow(stud_info[roll])
            
                print(f"Successfully exported to {filename}!")        
        elif a == '0':
            print("Logging out of Admin session... Goodbye!")
            break                     
             
elif Username=="user" and Password=="user123":
    print("1.View Students")
    print("2.Search Student")
    print("3.View Topper")
    print("4.Sort Students")
    print("0.Exit")
    u= input("Select:")
    #View Students
    while True:
        if u=='1':
            with open("student_info.json","r") as f:
                data=json.load(f)
                print(json.dumps(data, indent=4))
        elif u == '2':
            search_roll = input("Enter Roll No to search: ")
            
            # Check if the roll number exists in our dictionary
            if search_roll in stud_info:
                print("\n--- Student Found ---")
                # Pull the specific student's dictionary and print it nicely
                student_data = stud_info[search_roll]
                print(json.dumps(student_data, indent=4))
            else:
                print(f"Error: No record found for Roll No {search_roll}.")        
        elif u == '4':
            if not stud_info:
                print("No students to sort.")
            else:
                # Sort by converting the Roll No (key) to an integer
                # This ensures '2' comes before '10'
                sorted_tuples = sorted(stud_info.items(), key=lambda x: int(x[0]))
                
                # Convert back to a dictionary to display nicely
                sorted_stud_info = dict(sorted_tuples)
                
                print("\n--- Students Sorted by Roll No ---")
                print(json.dumps(sorted_stud_info, indent=4))
                
                # Optional: Save this sorted order permanently to the file
                save_choice = input("Save this sorted order to file? (y/n): ").lower()
                if save_choice == 'y':
                    with open("student_info.json", "w") as f:
                        json.dump(sorted_stud_info, f, indent=4)
                    print("File updated with sorted records.")
        elif u == '3':
            if not stud_info:
                print("No student data available.")
            else:
                # 1. Get all unique marks and sort them highest to lowest
                all_marks = sorted(set(info['Marks'] for info in stud_info.values()), reverse=True)
                
                # 2. Loop through the top 3 scores
                ranks = ["1st (Topper)", "2nd", "3rd"]
                
                print("\n" + "="*40)
                print("       TOP 3 RANK HOLDERS       ")
                print("="*40)

                # We loop through the top 3 scores (or fewer if there aren't many students)
                for i in range(min(3, len(all_marks))):
                    target_score = all_marks[i]
                    
                    # Find all students who have this specific score
                    winners = {roll: info for roll, info in stud_info.items() if info['Marks'] == target_score}
                    
                    print(f"\n--- {ranks[i]} Place | Score: {target_score} ---")
                    print(json.dumps(winners, indent=4))
                
                print("="*40)    
        elif u == '0':
            print("Logging out of User session... Goodbye!")   
            break                      
else:
    print("Invalid Credentials")
