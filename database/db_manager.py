"""
Database Manager for Assistly
Handles PostgreSQL connections and queries
"""
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.connection_params = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': os.getenv('POSTGRES_PORT', '5432'),
            'database': os.getenv('POSTGRES_DB', 'assistly_db'),
            'user': os.getenv('POSTGRES_USER', 'postgres'),
            'password': os.getenv('POSTGRES_PASSWORD', '')
        }
    
    def get_connection(self):
        """Create a new database connection"""
        return psycopg2.connect(**self.connection_params)
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute SELECT query and return results as list of dicts"""
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
    
    def execute_update(self, query: str, params: tuple = None) -> int:
        """Execute INSERT/UPDATE/DELETE and return affected rows"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount
        finally:
            conn.close()
    
    # Customer queries
    def get_customer(self, customer_id: str) -> Optional[Dict]:
        """Get customer by ID"""
        query = "SELECT * FROM customers WHERE customer_id = %s"
        results = self.execute_query(query, (customer_id,))
        return results[0] if results else None
    
    def get_customer_by_email(self, email: str) -> Optional[Dict]:
        """Get customer by email"""
        query = "SELECT * FROM customers WHERE email = %s"
        results = self.execute_query(query, (email,))
        return results[0] if results else None
    
    # Billing queries
    def get_billing_history(self, customer_id: str) -> List[Dict]:
        """Get billing history for customer"""
        query = """
            SELECT * FROM billing_history 
            WHERE customer_id = %s 
            ORDER BY billing_date DESC
        """
        return self.execute_query(query, (customer_id,))
    
    def get_failed_payments(self, customer_id: str) -> List[Dict]:
        """Get failed payments for customer"""
        query = """
            SELECT * FROM billing_history 
            WHERE customer_id = %s AND status = 'failed'
            ORDER BY billing_date DESC
        """
        return self.execute_query(query, (customer_id,))
    
    # Ticket queries
    def get_tickets(self, customer_id: str, status: str = None) -> List[Dict]:
        """Get tickets for customer, optionally filtered by status"""
        if status:
            query = """
                SELECT * FROM tickets 
                WHERE customer_id = %s AND status = %s
                ORDER BY created_at DESC
            """
            return self.execute_query(query, (customer_id, status))
        else:
            query = """
                SELECT * FROM tickets 
                WHERE customer_id = %s
                ORDER BY created_at DESC
            """
            return self.execute_query(query, (customer_id,))
    
    def create_ticket(self, customer_id: str, issue_type: str, 
                     subject: str, description: str, priority: str = 'medium') -> int:
        """Create new support ticket"""
        query = """
            INSERT INTO tickets (customer_id, issue_type, subject, description, priority)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING ticket_id
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (customer_id, issue_type, subject, description, priority))
                ticket_id = cursor.fetchone()[0]
                conn.commit()
                return ticket_id
        finally:
            conn.close()
    
    # Plan queries
    def get_plan(self, plan_id: str) -> Optional[Dict]:
        """Get plan details"""
        query = "SELECT * FROM plans WHERE plan_id = %s"
        results = self.execute_query(query, (plan_id,))
        return results[0] if results else None
    
    def get_all_plans(self) -> List[Dict]:
        """Get all active plans"""
        query = "SELECT * FROM plans WHERE active = TRUE ORDER BY price"
        return self.execute_query(query)