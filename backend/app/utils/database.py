import sqlite3
import json
import os
from typing import Dict, Any, Optional ,List
from datetime import datetime
import uuid

class Database:
    """Simple database without Redis dependency"""
    
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'stadium.db')
        self._init_db()
        print(f"✅ Database initialized at: {self.db_path}")
    
    def _init_db(self):
        """Create all tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table with accessibility_needs column
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'fan',
                language TEXT DEFAULT 'English',
                preferences TEXT,
                accessibility_needs TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_active TEXT DEFAULT CURRENT_TIMESTAMP,
                is_verified INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1
            )
        ''')
        
        # ✅ Add column if it doesn't exist (for existing databases)
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN accessibility_needs TEXT")
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        # Index for faster queries
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)")
        
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
    
    async def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email with JSON parsing"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            user_data = dict(row)
            # Parse JSON fields
            user_data['preferences'] = self._parse_json(user_data.get('preferences', '{}'))
            user_data['accessibility_needs'] = self._parse_json_list(user_data.get('accessibility_needs', '[]'))
            return user_data
        return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID with JSON parsing"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            user_data = dict(row)
            # Parse JSON fields
            user_data['preferences'] = self._parse_json(user_data.get('preferences', '{}'))
            user_data['accessibility_needs'] = self._parse_json_list(user_data.get('accessibility_needs', '[]'))
            return user_data
        return None
    
    def _parse_json(self, value: str) -> Dict:
        """Parse JSON string to dict"""
        if not value:
            return {}
        try:
            return json.loads(value)
        except:
            return {}
    
    def _parse_json_list(self, value: str) -> List:
        """Parse JSON string to list"""
        if not value:
            return []
        try:
            return json.loads(value)
        except:
            return []
    
    async def create_user(self, user_data: Dict) -> Dict:
        """Create new user with JSON serialization"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Convert dict/list to JSON strings
        preferences = json.dumps(user_data.get('preferences', {}))
        accessibility_needs = json.dumps(user_data.get('accessibility_needs', []))
        
        cursor.execute('''
            INSERT INTO users (
                id, name, email, password_hash, role, language, 
                preferences, accessibility_needs, created_at, last_active, 
                is_verified, is_active
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_data.get('id'),
            user_data.get('name'),
            user_data.get('email'),
            user_data.get('password_hash'),
            user_data.get('role', 'fan'),
            user_data.get('language', 'English'),
            preferences,
            accessibility_needs,
            user_data.get('created_at', datetime.utcnow().isoformat()),
            user_data.get('last_active', datetime.utcnow().isoformat()),
            1 if user_data.get('is_verified') else 0,
            1 if user_data.get('is_active') else 1
        ))
        conn.commit()
        conn.close()
        return user_data
    
    async def update_user(self, user_id: str, user_data: Dict) -> Optional[Dict]:
        """Update user data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        updates = []
        values = []
        
        for key, value in user_data.items():
            if key in ['name', 'language', 'preferences', 'accessibility_needs']:
                updates.append(f"{key} = ?")
                if key == 'preferences':
                    values.append(json.dumps(value))
                elif key == 'accessibility_needs':
                    values.append(json.dumps(value))
                else:
                    values.append(value)
        
        if updates:
            values.append(user_id)
            query = f"UPDATE users SET {', '.join(updates)}, last_active = CURRENT_TIMESTAMP WHERE id = ?"
            cursor.execute(query, values)
            conn.commit()
        conn.close()
        return await self.get_user_by_id(user_id)
    
    async def check_connection(self) -> bool:
        """Check database connection"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.close()
            return True
        except:
            return False
    
    async def close_connection(self):
        """Close database connection"""
        pass