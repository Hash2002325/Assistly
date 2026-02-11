"""
Setup script to initialize Assistly database
Run this once to create tables and populate mock data
"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def setup_database():
    # Connect to PostgreSQL (not to specific database yet)
    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'localhost'),
        port=os.getenv('POSTGRES_PORT', '5432'),
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', '')
    )
    conn.autocommit = True
    
    # Create database if it doesn't exist
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'assistly_db'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute("CREATE DATABASE assistly_db")
            print("✅ Created database: assistly_db")
        else:
            print("✅ Database already exists: assistly_db")
    
    conn.close()
    
    # Connect to the assistly_db database
    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'localhost'),
        port=os.getenv('POSTGRES_PORT', '5432'),
        database='assistly_db',
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', '')
    )
    
    # Read and execute schema
    with open('database/schema.sql', 'r') as f:
        schema = f.read()
    
    with conn.cursor() as cursor:
        cursor.execute(schema)
        conn.commit()
        print("✅ Created tables")
    
    # Read and execute mock data
    with open('database/mock_data.sql', 'r') as f:
        mock_data = f.read()
    
    with conn.cursor() as cursor:
        cursor.execute(mock_data)
        conn.commit()
        print("✅ Inserted mock data")
    
    conn.close()
    print("\n🎉 Database setup complete!")
    print("You can now run: python -c 'from database.db_manager import DatabaseManager; db = DatabaseManager(); print(db.get_customer(\"CUST001\"))'")

if __name__ == "__main__":
    setup_database()