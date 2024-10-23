import mysql.connector
from tabulate import tabulate

def connect_to_database():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="linkedin"
    )

def create_post(connection):
    cursor = connection.cursor()
    user_id = input("Enter user ID: ")
    post_content = input("Enter post content: ")
    post_date = input("Enter post date (YYYY-MM-DD): ")
    likes = input("Enter number of likes: ")
    last_liked_at = input("Enter last liked at date (YYYY-MM-DD): ")

    query = """INSERT INTO post (user_id, post_content, post_date, likes, last_liked_at) 
               VALUES (%s, %s, %s, %s, %s)"""
    values = (user_id, post_content, post_date, likes, last_liked_at)

    cursor.execute(query, values)
    connection.commit()
    post_id = cursor.lastrowid
    print("Post created successfully with ID:", post_id)
    cursor.close()
    return post_id

def read_post(connection):
    cursor = connection.cursor(dictionary=True)
    post_id = input("Enter post ID: ")
    query = "SELECT * FROM post WHERE post_id = %s"
    cursor.execute(query, (post_id,))
    result = cursor.fetchone()
    if result:
        print(tabulate([result], headers="keys", tablefmt="grid"))
    else:
        print("Post not found")
    cursor.close()

def update_post(connection):
    cursor = connection.cursor()
    post_id = input("Enter post ID to update: ")
    fields = ["user_id", "post_content", "post_date", "likes", "last_liked_at"]
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

    query = f"UPDATE post SET {', '.join(updates)} WHERE post_id = %s"
    values.append(post_id)

    cursor.execute(query, tuple(values))
    connection.commit()
    print("Post updated successfully")
    cursor.close()

def delete_post(connection):
    cursor = connection.cursor()
    post_id = input("Enter post ID to delete: ")
    query = "DELETE FROM post WHERE post_id = %s"
    cursor.execute(query, (post_id,))
    connection.commit()
    print("Post deleted successfully")
    cursor.close()

def main():
    connection = connect_to_database()
    print("Connected to the database successfully")
    
    while True:
        print("\nChoose an operation:")
        print("0: Create post")
        print("1: Read post")
        print("2: Update post")
        print("3: Delete post")
        print("4: Exit")

        choice = input("Enter your choice (0-4): ")

        if choice == '0':
            create_post(connection)
        elif choice == '1':
            read_post(connection)
        elif choice == '2':
            update_post(connection)
        elif choice == '3':
            delete_post(connection)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

    connection.close()
    print("Goodbye!")

if __name__ == "__main__":
    main()