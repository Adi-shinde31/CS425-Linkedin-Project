import mysql.connector
from tabulate import tabulate
from db import connect_to_database
from datetime import datetime
connection = connect_to_database()

def create_education(connection):
    # Create a cursor to execute SQL commands
    cursor = connection.cursor()

    # Prompt the user for education details
    user_id = input("\nEnter User ID: ")
    institution_id = input("Enter Institution ID: ")
    start = input("Enter Start Date (YYYY-MM-DD): ")
    end = input("Enter End Date (YYYY-MM-DD): ")
    course = input("Enter Course: ")

    # Validate that user ID, start date, and course are provided
    if(user_id==""):
        print("Error: User ID cannot be empty.")
        return
    if(start==""):
        print("Error: Start date cannot be empty.")
        return
    if(course==""):
        print("Error: Course cannot be empty.")
        return 

    # Validate user ID as an integer
    try:
        user_id = int(user_id)
    except ValueError:
        print("Error: User ID must be an integer.")
        return

    # Validate institution ID as an integer
    try:
        institution_id = int(institution_id)
    except ValueError:
        print("Error: Institution ID must be an integer.")
        return

    # Validate start date format
    try:
        start = datetime.strptime(start, "%Y-%m-%d")
    except ValueError:
        print("Error: Start date must be in YYYY-MM-DD format.")
        return

    # If end date is empty, insert record without it
    if(end==""):
        try:
            query = """INSERT INTO education (user_id, institution_id, start, course)
                   VALUES (%s, %s, %s, %s)"""
            values = (user_id, institution_id, start, course)
            cursor.execute(query, values)
            connection.commit()
            education_id = cursor.lastrowid
            print(f"\nEducation record created successfully with ID: {education_id}")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
        return education_id

    
    if end:
        try:
            end = datetime.strptime(end, "%Y-%m-%d")
        except ValueError:
            print("Error: End date must be in YYYY-MM-DD format.")
            return
    
    if (end!=""):  
        if start >= end:
            print("Error: Start date must be earlier than end date.")
            return
    try:
        query = """INSERT INTO education (user_id, institution_id, start, end, course)
                   VALUES (%s, %s, %s, %s, %s)"""
        values = (user_id, institution_id, start, end, course)
        cursor.execute(query, values)
        connection.commit()
        education_id = cursor.lastrowid
        print(f"\nEducation record created successfully with ID: {education_id}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
    return education_id


def read_education(connection):
    # Create a cursor to execute SQL commands with dictionary results for easier handling
    cursor = connection.cursor(dictionary=True)

    # Prompt the user for the user ID to retrieve education records
    user_id = input("\nEnter User ID to retrieve education records: ")
    
    # Validate that user_id is provided and is numeric
    if(user_id==""):
        print("Error: User ID cannot be empty.")
        return
    if not user_id.isdigit():
        print("Error: User ID must be a number.")
        return
    try:
        query = "SELECT * FROM education WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        if result:
            print(tabulate(result, headers="keys", tablefmt="grid"))
        else:
            print("No education records found for this user.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()


def get_all_education(connection):
    # Create a cursor to execute SQL commands with dictionary results for easy access to column names
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM education"
        cursor.execute(query)
        result = cursor.fetchall()
    
    # Handle any database errors that occur during retrieval
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        result = []

    # Check if there are any records to display
    if result:
        # Prepare the data for tabulate
        table_data = []
        for record in result:
            table_data.append([
                record['user_id'],
                record['institution_id'],
                record['start'],
                record['end'],
                record['course']
            ])

        # Print the table
        print(tabulate(table_data, headers=["user_id", "institution_id", "start", "end", "course"], tablefmt="grid"))
    else:
        print("No education records found.")

    cursor.close()

def update_education(connection):
    cursor = connection.cursor()

    # Prompt the user for the education ID to update
    education_id = input("Enter Education ID to update: ")
    
    # Validate that education_id is provided and is numeric
    if(education_id==""):
        print("Error: Education ID cannot be empty.")
        return
    
    if not education_id.isdigit():
        print("Error: Education ID must be a number.")
        return
    
    # Define the fields that can be updated
    fields = ["user_id", "institution_id", "start_date", "end_date", "course"]
    updates = []
    values = []
    for field in fields:
        value = input(f"Enter new {field} (leave blank to skip): ")
        if value:
            if field in ["user_id", "institution_id"]:
                if not value.isdigit():
                    print(f"Error: {field} must be a number.")
                    return
                value = int(value)
            elif field in ["start_date", "end_date"]:
                try:
                    value = datetime.strptime(value, "%Y-%m-%d")
                except ValueError:
                    print(f"Error: {field} must be in YYYY-MM-DD format.")
                    return
            updates.append(f"{field} = %s")
            values.append(value)

    # Check if there are any fields to update
    if not updates:
        print("No fields to update")
        return
    
    # Attempt to update the education record in the database
    try:
        query = f"UPDATE education SET {', '.join(updates)} WHERE id = %s"
        values.append(education_id)
        cursor.execute(query, tuple(values))
        connection.commit()
        print("\nEducation record updated successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

def delete_education(connection):
    # Create a cursor to execute SQL commands
    cursor = connection.cursor()
    
    # Prompt the user for the education ID to delete
    education_id = input("Enter Education ID to delete: ")

    # Validate that education_id is provided and is numeric
    if(education_id==""):
        print("Error: Education ID cannot be empty.")
        return
    if not education_id.isdigit():
        print("Error: Education ID must be a number.")
        return
    
    # Attempt to delete the education record from the database
    try:
        query = "DELETE FROM education WHERE id = %s"
        cursor.execute(query, (education_id,))
        connection.commit()
        print("Education record deleted successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

def education_menu():
    connection = connect_to_database()

    # Exit if the connection to the database was unsuccessful
    if not connection:
        return

    while True:
        print("\nChoose an operation:")
        print("1: Create education record")
        print("2: Read education records")
        print("3. Get all education records")
        print("4: Update education record")
        print("5: Delete education record")
        print("0: Exit")

        choice = input("\nEnter your choice (0-4): ")

        if choice == '1':
            create_education(connection)
        elif choice == '2':
            read_education(connection)
        elif choice == '3':
            get_all_education(connection)
        elif choice == '4':
            update_education(connection)
        elif choice == '5':
            delete_education(connection)
        elif choice == '0':
            connection.close()
            print("Database Disconnected Successfully!")
            print("\nExit from Education Menu.")
            print("\n      - X - X - X -")
            return
        else:
            print("\nInvalid choice. Please try again.")
