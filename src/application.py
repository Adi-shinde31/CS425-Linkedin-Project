import mysql.connector
from tabulate import tabulate

def connect_to_database():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="linkedin"
    )

def create_job(connection):
    cursor = connection.cursor()
    institution_id = input("Enter institution ID: ")
    job_title = input("Enter job title: ")
    description = input("Enter description: ")
    job_type = input("Enter type: ")

    query = """INSERT INTO job (institution_id, job_title, description, type) 
               VALUES (%s, %s, %s, %s)"""
    values = (institution_id, job_title, description, job_type)

    cursor.execute(query, values)
    connection.commit()
    job_id = cursor.lastrowid
    print("Job created successfully with ID:", job_id)
    cursor.close()
    return job_id

def read_job(connection):
    cursor = connection.cursor(dictionary=True)
    job_id = input("Enter job ID: ")
    query = "SELECT * FROM job WHERE job_id = %s"
    cursor.execute(query, (job_id,))
    result = cursor.fetchone()
    if result:
        print(tabulate([result], headers="keys", tablefmt="grid"))
    else:
        print("Job not found")
    cursor.close()

def update_job(connection):
    cursor = connection.cursor()
    job_id = input("Enter job ID to update: ")
    fields = ["institution_id", "job_title", "description", "type"]
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

    query = f"UPDATE job SET {', '.join(updates)} WHERE job_id = %s"
    values.append(job_id)

    cursor.execute(query, tuple(values))
    connection.commit()
    print("Job updated successfully")
    cursor.close()

def delete_job(connection):
    cursor = connection.cursor()
    job_id = input("Enter job ID to delete: ")
    query = "DELETE FROM job WHERE job_id = %s"
    cursor.execute(query, (job_id,))
    connection.commit()
    print("Job deleted successfully")
    cursor.close()

def main():
    connection = connect_to_database()
    print("Connected to the database successfully")
    
    while True:
        print("\nChoose an operation:")
        print("0: Create job")
        print("1: Read job")
        print("2: Update job")
        print("3: Delete job")
        print("4: Exit")

        choice = input("Enter your choice (0-4): ")

        if choice == '0':
            create_job(connection)
        elif choice == '1':
            read_job(connection)
        elif choice == '2':
            update_job(connection)
        elif choice == '3':
            delete_job(connection)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

    connection.close()
    print("Goodbye!")

if __name__ == "__main__":
    main()