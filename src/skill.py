import mysql.connector
from tabulate import tabulate

def connect_to_database():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="linkedin"
    )

def create_skill(connection):
    cursor = connection.cursor()
    skill_name = input("Enter skill name: ")

    query = "INSERT INTO skill (skill_name) VALUES (%s)"
    values = (skill_name,)

    cursor.execute(query, values)
    connection.commit()
    skill_id = cursor.lastrowid
    print("Skill created successfully with ID:", skill_id)
    cursor.close()
    return skill_id

def read_skill(connection):
    cursor = connection.cursor(dictionary=True)
    skill_id = input("Enter skill ID: ")
    query = "SELECT * FROM skill WHERE skill_id = %s"
    cursor.execute(query, (skill_id,))
    result = cursor.fetchone()
    if result:
        print(tabulate([result], headers="keys", tablefmt="grid"))
    else:
        print("Skill not found")
    cursor.close()

def update_skill(connection):
    cursor = connection.cursor()
    skill_id = input("Enter skill ID to update: ")
    new_skill_name = input("Enter new skill name (leave blank to skip): ")

    if not new_skill_name:
        print("No fields to update")
        return

    query = "UPDATE skill SET skill_name = %s WHERE skill_id = %s"
    values = (new_skill_name, skill_id)

    cursor.execute(query, values)
    connection.commit()
    print("Skill updated successfully")
    cursor.close()

def delete_skill(connection):
    cursor = connection.cursor()
    skill_id = input("Enter skill ID to delete: ")
    query = "DELETE FROM skill WHERE skill_id = %s"
    cursor.execute(query, (skill_id,))
    connection.commit()
    print("Skill deleted successfully")
    cursor.close()

def main():
    connection = connect_to_database()
    print("Connected to the database successfully")
    
    while True:
        print("\nChoose an operation:")
        print("0: Create skill")
        print("1: Read skill")
        print("2: Update skill")
        print("3: Delete skill")
        print("4: Exit")

        choice = input("Enter your choice (0-4): ")

        if choice == '0':
            create_skill(connection)
        elif choice == '1':
            read_skill(connection)
        elif choice == '2':
            update_skill(connection)
        elif choice == '3':
            delete_skill(connection)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

    connection.close()
    print("Goodbye!")

if __name__ == "__main__":
    main()