# # import mysql.connector
# # from passlib.context import CryptContext

# # # Connection with MySQL Database
# # db = mysql.connector.connect(host = "localhost", user="root", password="1234")
# # cur = db.cursor()

# # # Create database if doesn't exists
# # cur.execute("CREATE DATABASE IF NOT EXISTS library_ms")
# # cur.close()

# # # Connect to the newly created databas
# # db = mysql.connector.connect(host = "localhost", user="root", password="1234", database="iitb")
# # cur = db.cursor()

# # # Create table "users"
# # cur.execute('''CREATE TABLE IF NOT EXISTS users(
# #             id INT AUTO_INCREMENT PRIMARY KEY,
# #             username VARCHAR(255) NOT NULL,
# #             password VARCHAR(255) NOT NULL,
# #             role ENUM('LIBRARIAN','MEMBER') NOT NULL,
# #             created_at TIMESTAMP NOT NULL
# #             )
# # ''')

# # # Create table "books"
# # cur.execute('''CREATE TABLE IF NOT EXISTS books(
# #             id INT AUTO_INCREMENT PRIMARY KEY,
# #             title VARCHAR(255) NOT NULL,
# #             author VARCHAR(255) NOT NULL,
# #             status ENUM('AVAILABLE', 'BORROWED') NOT NULL,
# #             created_at TIMESTAMP NOT NULL
# #             )
# # ''')

# # # Create table "borrowed_books"
# # cur.execute('''CREATE TABLE IF NOT EXISTS borrowed_books(
# #             id INT AUTO_INCREMENT PRIMARY KEY,
# #             book_id INT,
# #             user_id INT,
# #             borrowed_at TIMESTAMP NOT NULL,
# #             returned_at TIMESTAMP,
# #             FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE ON UPDATE CASCADE,
# #             FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
# #             )
# # ''')

# # # Create table "activity_log"
# # cur.execute('''CREATE TABLE IF NOT EXISTS activity_log(
# #             id INT AUTO_INCREMENT PRIMARY KEY,
# #             user_id INT,
# #             action VARCHAR(255),
# #             created_at TIMESTAMP,
# #             FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
# #             )
# # ''')

# # # Close the database cursor
# # cur.close()


# # def get_user(user_id):
# #     cur = db.cursor()

# #     # Check if username already exist in the database
# #     select_query = "SELECT username,role FROM users WHERE id=%s"
# #     cur.execute(select_query, (user_id,))
# #     user = cur.fetchone()
# #     return user


# import psycopg2
# from psycopg2 import sql
# from datetime import datetime

# # Connection details
# PASSWORD = '@Jaishreeram'  # Replace with your actual password
# DATABASE_URL = f"postgresql://postgres.sarcngbctfnzwpabtlec:{PASSWORD}@aws-0-ap-south-1.pooler.supabase.com:6543/postgres?pgbouncer=true"
# DIRECT_URL = f"postgresql://postgres.sarcngbctfnzwpabtlec:{PASSWORD}@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"

# # Function to connect to the database
# def connect_to_database(url):
#     try:
#         return psycopg2.connect(url)
#     except Exception as e:
#         print(f"Connection error: {e}")
#         return None

# # Connect using connection pooling
# db = connect_to_database(DATABASE_URL)
# if db is not None:
#     cur = db.cursor()

#     # Create database if it doesn't exist (note: this won't work in PostgreSQL from a connected session)
#     # You'll need to ensure the database exists beforehand.
#     # cur.execute("CREATE DATABASE IF NOT EXISTS library_ms")  # Uncomment this if you have the right permissions

#     # Close the cursor and connection
#     cur.close()
#     db.close()

# # Connect to the newly created database using direct URL for migrations
# db_migrations = connect_to_database(DIRECT_URL)
# if db_migrations is not None:
#     cur_migrations = db_migrations.cursor()

#     # Create database and tables if needed
#     cur_migrations.execute('''
#     CREATE TABLE IF NOT EXISTS users(
#         id SERIAL PRIMARY KEY,
#         username VARCHAR(255) NOT NULL UNIQUE,
#         password VARCHAR(255) NOT NULL,
#         role VARCHAR(50) CHECK (role IN ('LIBRARIAN', 'MEMBER')) NOT NULL,
#         created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
#     )
#     ''')

#     cur_migrations.execute('''
#     CREATE TABLE IF NOT EXISTS books(
#         id SERIAL PRIMARY KEY,
#         title VARCHAR(255) NOT NULL,
#         author VARCHAR(255) NOT NULL,
#         status VARCHAR(50) CHECK (status IN ('AVAILABLE', 'BORROWED')) NOT NULL,
#         created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
#     )
#     ''')

#     cur_migrations.execute('''
#     CREATE TABLE IF NOT EXISTS borrowed_books(
#         id SERIAL PRIMARY KEY,
#         book_id INT REFERENCES books(id) ON DELETE CASCADE ON UPDATE CASCADE,
#         user_id INT REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
#         borrowed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#         returned_at TIMESTAMP
#     )
#     ''')

#     cur_migrations.execute('''
#     CREATE TABLE IF NOT EXISTS activity_log(
#         id SERIAL PRIMARY KEY,
#         user_id INT REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
#         action VARCHAR(255),
#         created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
#     )
#     ''')

#     # Commit the changes
#     db_migrations.commit()

#     # Close the database cursor and connection
#     cur_migrations.close()
#     db_migrations.close()

# def get_user(user_id):
#     try:
#         db = connect_to_database(DATABASE_URL)  # Using the pooled connection
#         if db is not None:
#             cur = db.cursor()

#             # Check if username already exists in the database
#             select_query = "SELECT username, role FROM users WHERE id = %s"
#             cur.execute(select_query, (user_id,))
#             user = cur.fetchone()
#             return user

#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         if cur:
#             cur.close()
#         if db:
#             db.close()


import psycopg2
from psycopg2 import sql
from datetime import datetime
from urllib.parse import quote

# Connection details
PASSWORD = quote('@Jaishreeram')  # URL-encoded password
DATABASE_URL = f"postgresql://postgres.sarcngbctfnzwpabtlec:{PASSWORD}@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
DIRECT_URL = f"postgresql://postgres.sarcngbctfnzwpabtlec:{PASSWORD}@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"

# Function to connect to the database
def connect_to_database(url):
    try:
        connection = psycopg2.connect(url)
        print("Database connection successful.")
        return connection
    except Exception as e:
        print(f"Connection error: {e}")
        return None

# Connect using connection pooling
db = connect_to_database(DATABASE_URL)

if db is not None:
    cur = db.cursor()

    # Create tables if needed
    try:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(50) CHECK (role IN ('LIBRARIAN', 'MEMBER')) NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("Users table created successfully.")

        cur.execute('''
        CREATE TABLE IF NOT EXISTS books(
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            status VARCHAR(50) CHECK (status IN ('AVAILABLE', 'BORROWED')) NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("Books table created successfully.")

        cur.execute('''
        CREATE TABLE IF NOT EXISTS borrowed_books(
            id SERIAL PRIMARY KEY,
            book_id INT REFERENCES books(id) ON DELETE CASCADE ON UPDATE CASCADE,
            user_id INT REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
            borrowed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            returned_at TIMESTAMP
        )
        ''')
        print("Borrowed books table created successfully.")

        cur.execute('''
        CREATE TABLE IF NOT EXISTS activity_log(
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
            action VARCHAR(255),
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("Activity log table created successfully.")

        # Commit the changes
        db.commit()

    except Exception as e:
        print(f"Error during table creation: {e}")

    # Close the cursor and connection
    cur.close()
    db.close()

# Connect to the newly created database using direct URL for migrations
db_migrations = connect_to_database(DIRECT_URL)

if db_migrations is not None:
    cur_migrations = db_migrations.cursor()

    # Example: Insert a sample user and check if it's inserted
    try:
        cur_migrations.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s) RETURNING id",
                               ('test_user', 'password123', 'MEMBER'))
        user_id = cur_migrations.fetchone()[0]
        db_migrations.commit()
        print(f"Inserted user with ID: {user_id}")

        # Retrieve the inserted user
        cur_migrations.execute("SELECT username, role FROM users WHERE id = %s", (user_id,))
        user = cur_migrations.fetchone()
        print(f"Retrieved user: {user}")

    except Exception as e:
        print(f"Error during data insertion: {e}")
    
    # Close the database cursor and connection
    cur_migrations.close()
    db_migrations.close()

def get_user(user_id):
    try:
        db = connect_to_database(DATABASE_URL)  # Using the pooled connection
        if db is not None:
            cur = db.cursor()

            # Check if username already exists in the database
            select_query = "SELECT username, role FROM users WHERE id = %s"
            cur.execute(select_query, (user_id,))
            user = cur.fetchone()
            return user

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cur:
            cur.close()
        if db:
            db.close()
