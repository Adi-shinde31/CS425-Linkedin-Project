import mysql.connector
from tabulate import tabulate
from db import connect_to_database
connection = connect_to_database()

def create_experience(connection):
    cursor = connection.cursor()

    user_id = input("\nEnter User ID: ")
    institution_id = input("Enter Institution ID: ")
    title = input("Enter Title: ")
    start = input("Enter Start Date (YYYY-MM-DD): ")
    end = input("Enter End Date (YYYY-MM-DD): ")
    description = input("Enter Description: ")

    # Error handling for date validation
    if(end==""):
        query = """INSERT INTO experience (user_id, institution_id, start, description, title)
               VALUES (%s, %s, %s, %s, %s)"""
        values = (user_id, institution_id, start, description, title)
        cursor.execute(query, values)
        connection.commit()
        experience_id = cursor.lastrowid
        print(f"Experience created successfully with ID: {experience_id}")
        cursor.close()
        return
    if(end!=""):
        if start >= end:
            print("Error: Start date must be earlier than end date.")
            return
    query = """INSERT INTO experience (user_id, institution_id, start, end, description, title)
               VALUES (%s, %s, %s, %s, %s, %s)"""
    values = (user_id, institution_id, start, end, description, title)

    cursor.execute(query, values)
    connection.commit()
    experience_id = cursor.lastrowid

    print(f"\nExperience created successfully with ID: {experience_id}")
    cursor.close()

def read_experience(connection):
    cursor = connection.cursor(dictionary=True)

    user_id = input("\nEnter User ID to retrieve experiences: ")
    query = "SELECT * FROM experience WHERE user_id = %s"

    cursor.execute(query, (user_id,))
    results = cursor.fetchall()

    if results:
        print(tabulate(results, headers="keys", tablefmt="grid"))
    else:
        print("No experiences found for this user.")

    cursor.close()

def update_experience(connection):
    cursor = connection.cursor()

    experience_id = input("Enter Experience ID to update: ")
    fields = ["user_id", "institution_id", "title", "company", "location", "start_date", "end_date", "description"]
    updates = []
    values = []

    for field in fields:
        value = input(f"Enter new {field} (leave blank to skip): ")
        if value:
            updates.append(f"{field} = %s")
            values.append(value)

    if not updates:
        print("No fields to update")
        return

    query = f"UPDATE experience SET {', '.join(updates)} WHERE id = %s"
    values.append(experience_id)

    cursor.execute(query, tuple(values))
    connection.commit()
    print("Experience updated successfully")
    cursor.close()

def delete_experience(connection):
    cursor = connection.cursor()
    
    exp_id = input("Enter Experience ID to delete: ")
    query = "DELETE FROM experience WHERE exp_id = %s"
    cursor.execute(query, (exp_id,))
    connection.commit()

    print(f"Experience with ID {exp_id} deleted successfully")
    cursor.close()

def experience_menu():
    connection = connect_to_database()

    if not connection:
        return

    while True:
        print("\nChoose an operation:")
        print("1: Create Experience")
        print("2: Read Experiences")
        print("3: Update Experience")
        print("4: Delete Experience")
        print("0: Exit")

        choice = input("\nEnter your choice (0-4): ")

        if choice == '1':
            create_experience(connection)
        elif choice == '2':
            read_experience(connection)
        elif choice == '3':
            update_experience(connection)
        elif choice == '4':
            delete_experience(connection)
        elif choice == '0':
            connection.close()
            print("Database Disconnected Successfully!")
            print("\nExit from Experience Menu.")
            print("\n      - X - X - X -")
            return
        else:
            print("\nInvalid choice. Please try again.")
