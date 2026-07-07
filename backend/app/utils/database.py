import sqlite3
import json
import os
from typing import Dict, Any, Optional
from datetime import datetime
import hashlib
import uuid

class Database:
    def __init__(self):
        # Database file will be created in the backend folder
        self.db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'stadium.db')
        self._init_db()
        print(f"✅ Database initialized at: {self.db_path}")
    
    def _init_db(self):
        """Create all tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'fan',
                language TEXT DEFAULT 'English',
                preferences TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_active TEXT DEFAULT CURRENT_TIMESTAMP,
                is_verified INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1
            )
        ''')
        
        # Stadium data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stadium_data (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                capacity INTEGER DEFAULT 80000,
                current_attendance INTEGER DEFAULT 0,
                event_name TEXT DEFAULT 'FIFA World Cup',
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Crowd data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crowd_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                section TEXT NOT NULL,
                density REAL DEFAULT 0,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Queue data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS queue_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                establishment TEXT NOT NULL,
                queue_length INTEGER DEFAULT 0,
                wait_time INTEGER DEFAULT 0,
                status TEXT DEFAULT 'available',
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Emergency alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emergency_alerts (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                severity TEXT DEFAULT 'medium',
                location TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'active',
                reported_by TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                resolved_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    # ============ USER METHODS ============
    
    async def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    async def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    async def create_user(self, user_data: Dict) -> Dict:
        """Create new user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Generate ID if not provided
        if not user_data.get('id'):
            user_data['id'] = str(uuid.uuid4())
        
        cursor.execute('''
            INSERT INTO users (id, name, email, password_hash, role, language, preferences)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_data.get('id'),
            user_data.get('name'),
            user_data.get('email'),
            user_data.get('password_hash'),
            user_data.get('role', 'fan'),
            user_data.get('language', 'English'),
            json.dumps(user_data.get('preferences', {}))
        ))
        conn.commit()
        conn.close()
        return user_data
    
    async def update_user(self, user_id: str, user_data: Dict) -> Optional[Dict]:
        """Update user data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        updates = []
        values = []
        
        for key, value in user_data.items():
            if key in ['name', 'language', 'preferences']:
                updates.append(f"{key} = ?")
                if key == 'preferences':
                    values.append(json.dumps(value))
                else:
                    values.append(value)
        
        if not updates:
            conn.close()
            return await self.get_user_by_id(user_id)
        
        values.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)}, last_active = CURRENT_TIMESTAMP WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        
        return await self.get_user_by_id(user_id)
    
    # ============ STADIUM METHODS ============
    
    async def get_stadium_data(self) -> Dict:
        """Get stadium data"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stadium_data LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        
        # Create default stadium data
        default_data = {
            'id': 'stadium_1',
            'name': 'FIFA World Cup Stadium',
            'capacity': 80000,
            'current_attendance': 45000,
            'event_name': 'FIFA World Cup',
            'updated_at': datetime.utcnow().isoformat()
        }
        
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO stadium_data (id, name, capacity, current_attendance, event_name)
            VALUES (?, ?, ?, ?, ?)
        ''', (default_data['id'], default_data['name'], default_data['capacity'], 
              default_data['current_attendance'], default_data['event_name']))
        conn.commit()
        conn.close()
        
        return default_data
    
    # ============ CROWD METHODS ============
    
    async def save_crowd_data(self, section: str, density: float):
        """Save crowd data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO crowd_data (section, density)
            VALUES (?, ?)
        ''', (section, density))
        conn.commit()
        conn.close()
    
    async def get_latest_crowd_data(self) -> list:
        """Get latest crowd data"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM crowd_data 
            ORDER BY timestamp DESC 
            LIMIT 50
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    # ============ QUEUE METHODS ============
    
    async def save_queue_data(self, establishment: str, queue_length: int, wait_time: int, status: str):
        """Save queue data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO queue_data (establishment, queue_length, wait_time, status)
            VALUES (?, ?, ?, ?)
        ''', (establishment, queue_length, wait_time, status))
        conn.commit()
        conn.close()
    
    async def get_latest_queue_data(self) -> list:
        """Get latest queue data"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM queue_data 
            ORDER BY timestamp DESC 
            LIMIT 20
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    # ============ EMERGENCY METHODS ============
    
    async def save_emergency_alert(self, alert_data: Dict) -> Dict:
        """Save emergency alert"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        alert_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO emergency_alerts (id, type, severity, location, description, status, reported_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            alert_id,
            alert_data.get('type'),
            alert_data.get('severity', 'medium'),
            alert_data.get('location'),
            alert_data.get('description'),
            'active',
            alert_data.get('reported_by')
        ))
        conn.commit()
        conn.close()
        
        return {**alert_data, 'id': alert_id, 'status': 'active'}
    
    async def get_active_emergencies(self) -> list:
        """Get active emergencies"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM emergency_alerts 
            WHERE status = 'active'
            ORDER BY timestamp DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    async def resolve_emergency(self, alert_id: str) -> bool:
        """Resolve an emergency"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE emergency_alerts 
            SET status = 'resolved', resolved_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (alert_id,))
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0
    
    async def check_connection(self) -> bool:
        """Check database connection"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            conn.close()
            return True
        except:
            return False
    
    async def close_connection(self):
        """Close database connection (for SQLite, nothing to close)"""
        pass