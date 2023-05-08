import psycopg2
from itertools import product

db_params = {
    "host": "127.0.0.1",
    "port": 5432,
    "user": "postgres",
    "password": "password123",
    "database": "postgres",
}

conn = psycopg2.connect(**db_params)
conn.autocommit = True

cur = conn.cursor()
cur.execute("SELECT 1 FROM pg_database WHERE datname='backend_db'")
if cur.fetchone():
    cur.execute(
        "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'backend_db';"
    )
    cur.execute("DROP DATABASE backend_db")
    print("backend_db database dropped successfully")

cur.execute("CREATE DATABASE backend_db")
print("backend_db database created successfully")

cur.execute(
    "SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'users')"
)
exists = cur.fetchone()[0]
if not exists:
    cur.execute(
        """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            username VARCHAR(255) NOT NULL,
            is_2fa_enabled BOOLEAN NOT NULL
        )
    """
    )
    print("users table created successfully")

emails = ["test1@example.com", "test2@example.com", "test3@example.com"]
passwords = ["password1", "password2", "password3"]
usernames = ["User1", "User2", "User3"]
is_2fa_enabled_values = [True, False]

values = product(emails, passwords, usernames, is_2fa_enabled_values)

cur.executemany(
    """
    INSERT INTO users (email, password, username, is_2fa_enabled)
    VALUES (%s, %s, %s, %s)
""",
    values,
)
print("users table populated successfully")

cur.close()
conn.close()
