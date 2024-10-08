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
        return psycopg2.connect(url)
    except Exception as e:
        print(f"Connection error: {e}")
        return None

# Connect using connection pooling
db = connect_to_database(DATABASE_URL)
if db is not None:
    cur = db.cursor()

    # Note: In PostgreSQL, you cannot create a database from an active session. 
    # Ensure the database exists beforehand.

    # Close the cursor and connection
    cur.close()
    db.close()

# Connect to the newly created database using direct URL for migrations
db_migrations = connect_to_database(DIRECT_URL)
if db_migrations is not None:
    cur_migrations = db_migrations.cursor()

    # Create tables if needed
    cur_migrations.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(50) CHECK (role IN ('LIBRARIAN', 'MEMBER')) NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cur_migrations.execute('''
    CREATE TABLE IF NOT EXISTS books(
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        author VARCHAR(255) NOT NULL,
        status VARCHAR(50) CHECK (status IN ('AVAILABLE', 'BORROWED')) NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cur_migrations.execute('''
    CREATE TABLE IF NOT EXISTS borrowed_books(
        id SERIAL PRIMARY KEY,
        book_id INT REFERENCES books(id) ON DELETE CASCADE ON UPDATE CASCADE,
        user_id INT REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
        borrowed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        returned_at TIMESTAMP
    )
    ''')

    cur_migrations.execute('''
    CREATE TABLE IF NOT EXISTS activity_log(
        id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
        action VARCHAR(255),
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Commit the changes
    db_migrations.commit()

    # Close the database cursor and connection
    cur_migrations.close()
    db_migrations.close()

def get_user(user_id):
    db = connect_to_database(DATABASE_URL)  # Using the pooled connection
    cur = None
    try:
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
