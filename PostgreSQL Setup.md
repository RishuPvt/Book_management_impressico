# Flask Book Management – PostgreSQL Setup

This project uses **Flask + PostgreSQL** for a simple book management system.

This README explains:
- How to set up PostgreSQL locally (default & recommended)
- When and why `pg_hba.conf` changes are needed
- Database and user creation steps

## 1️⃣ Install PostgreSQL

sudo apt update
sudo apt install postgresql postgresql-contrib

#  2️⃣ Switch to PostgreSQL Admin User

sudo -i -u postgres
psql

postgres is the default PostgreSQL superuser
This uses peer authentication (Linux user → PostgreSQL user)

# 3️⃣ Set Password for PostgreSQL Superuser

ALTER USER postgres WITH PASSWORD 'yourpassword'; -- Sets password for postgres user

This password is required for:
Flask apps
psycopg2
TCP/IP connections

# 4️⃣ Create Application Database User (Recommended)

CREATE ROLE book_user LOGIN PASSWORD 'bookpassword'; -- Creates a dedicated DB user

⚠️ Avoid using postgres user in applications.

# 5️⃣ Create Database
CREATE DATABASE book_db OWNER book_user; -- Creates database owned by app user

# 6️⃣ Connect to the Database
\c book_db; -- Switches connection to book_db

# 7️⃣ Create Book Table

CREATE TABLE book (
    id SERIAL PRIMARY KEY,                 -- Auto-increment primary key
    publisher VARCHAR(255) NOT NULL,       -- Publisher name
    name VARCHAR(255) NOT NULL,            -- Book name
    date DATE NOT NULL,                    -- Published date
    cost DECIMAL(10, 2) NOT NULL           -- Book cost
);

# 8️⃣ Default pg_hba.conf (NO CHANGES REQUIRED for Local Setup)

By default, PostgreSQL allows:

Linux user login via peer
Local TCP connections via password (SCRAM)

Default configuration works for:

Flask running on the same machine
psycopg2
Local Docker containers

✅ No changes required for local development

# 9️⃣ Flask Database Configuration (Local)
db_config = {
    "host": "localhost",
    "user": "book_user",
    "password": "bookpassword",
    "dbname": "book_db"
 }

🔐 pg_hba.conf Changes (ONLY for Remote PostgreSQL)

⚠️ Required ONLY if PostgreSQL is on a different machine

Examples:

Cloud PostgreSQL
Separate VM
Kubernetes
Remote server

Example change (remote access):
host    book_db     book_user     0.0.0.0/0     scram-sha-256


# After editing:

sudo systemctl reload postgresql

❗ Do NOT open 0.0.0.0/0 in production without firewall rules