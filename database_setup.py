import sqlite3

# Connect to SQLite database (creates a file database.db)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Drop existing tables if they exist (to avoid conflicts)
cursor.execute("DROP TABLE IF EXISTS institutions")
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("DROP TABLE IF EXISTS certificates")
cursor.execute("DROP TABLE IF EXISTS admin")
cursor.execute("DROP TABLE IF EXISTS complaints") 

# Create a table for institution registration with all required fields
cursor.execute("""
    CREATE TABLE institutions (
        institution_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        affiliation TEXT NOT NULL,
        reg_number TEXT NOT NULL UNIQUE,
        date_of_establishment TEXT NOT NULL,
        institution_type TEXT NOT NULL,
        street_address TEXT NOT NULL,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        postal_code TEXT NOT NULL,
        country TEXT NOT NULL,
        official_email TEXT NOT NULL UNIQUE,
        phone_number TEXT NOT NULL,
        admin_name TEXT NOT NULL,
        admin_designation TEXT NOT NULL,
        admin_email TEXT NOT NULL UNIQUE,
        admin_phone TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        verified INTEGER DEFAULT 0  -- 0 = Not verified, 1 = Verified
    )
""")

# Create a table for user registration (login credentials)
cursor.execute("""
    CREATE TABLE users (
        user_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
""")

# Create a table for storing issued certificates
cursor.execute("""
    CREATE TABLE certificates (
        cert_id TEXT PRIMARY KEY,
        email TEXT NOT NULL,
        course TEXT NOT NULL,
        FOREIGN KEY (email) REFERENCES users(email)
    )
""")

# Create a table for admin login credentials
cursor.execute("""
    CREATE TABLE admin (
        admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
""")

# Create a table for storing user complaints
cursor.execute("""
   CREATE TABLE complaints (
        complaint_id TEXT PRIMARY KEY,
        user_email TEXT NOT NULL,
        complaint_text TEXT NOT NULL,
        submission_date TEXT NOT NULL
    )
""")

conn.commit()
conn.close()

print("Database setup complete.")
