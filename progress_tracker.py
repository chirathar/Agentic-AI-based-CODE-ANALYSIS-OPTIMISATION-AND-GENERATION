import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class ProgressTracker:
    """SQLite-based learning progress tracking system"""
    
    def __init__(self, db_path: str = 'learning_progress.db'):
        """Initialize the progress tracker with SQLite database"""
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                skill_level TEXT DEFAULT 'beginner',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                difficulty TEXT,
                language TEXT,
                concept TEXT,
                expected_patterns TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Task completions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task_id INTEGER NOT NULL,
                code TEXT,
                feedback TEXT,
                score REAL,
                concept_gaps TEXT,
                time_taken INTEGER,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (task_id) REFERENCES tasks(id)
            )
        ''')
        
        # Progress summary table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                weak_areas TEXT,
                strong_areas TEXT,
                total_tasks_completed INTEGER DEFAULT 0,
                avg_score REAL DEFAULT 0,
                recommended_topics TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_or_create_user(self, username: str) -> int:
        """Get or create user, return user_id"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        
        if result:
            conn.close()
            return result[0]
        
        cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
        user_id = cursor.lastrowid
        
        # Create progress entry
        cursor.execute(
            'INSERT INTO progress (user_id, weak_areas, strong_areas) VALUES (?, ?, ?)',
            (user_id, json.dumps([]), json.dumps([]))
        )
        
        conn.commit()
        conn.close()
        return user_id
    
    def save_completion(self, user_id: int, task_id: int, code: str, 
                       feedback: str, score: float, concept_gaps: List[str],
                       time_taken: int = 0) -> int:
        """Save task completion record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO completions 
            (user_id, task_id, code, feedback, score, concept_gaps, time_taken)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, task_id, code, feedback, score, json.dumps(concept_gaps), time_taken))
        
        completion_id = cursor.lastrowid
        
        # Update user progress
        self._update_user_progress(cursor, user_id)
        
        conn.commit()
        conn.close()
        return completion_id
    
    def _update_user_progress(self, cursor, user_id: int):
        """Update user progress summary"""
        cursor.execute('''
            SELECT AVG(score), COUNT(*) FROM completions WHERE user_id = ?
        ''', (user_id,))
        avg_score, total_tasks = cursor.fetchone()
        avg_score = avg_score or 0
        total_tasks = total_tasks or 0
        
        # Get weak areas from concept gaps
        cursor.execute('''
            SELECT concept_gaps FROM completions 
            WHERE user_id = ? AND concept_gaps IS NOT NULL
            ORDER BY completed_at DESC LIMIT 10
        ''', (user_id,))
        
        weak_areas = {}
        for row in cursor.fetchall():
            if row[0]:
                gaps = json.loads(row[0])
                for gap in gaps:
                    weak_areas[gap] = weak_areas.get(gap, 0) + 1
        
        weak_areas_sorted = sorted(weak_areas.items(), key=lambda x: x[1], reverse=True)
        weak_areas_list = [area[0] for area in weak_areas_sorted[:5]]
        
        # Get strong areas from high scores
        cursor.execute('''
            SELECT concept FROM tasks t
            JOIN completions c ON t.id = c.task_id
            WHERE c.user_id = ? AND c.score >= 80
            GROUP BY t.concept
        ''', (user_id,))
        
        strong_areas = [row[0] for row in cursor.fetchall()]
        
        cursor.execute('''
            UPDATE progress 
            SET weak_areas = ?, strong_areas = ?, total_tasks_completed = ?, avg_score = ?,
                last_updated = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (json.dumps(weak_areas_list), json.dumps(strong_areas), total_tasks, avg_score, user_id))
    
    def get_user_progress(self, user_id: int) -> Dict:
        """Get user progress summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT weak_areas, strong_areas, total_tasks_completed, avg_score, recommended_topics
            FROM progress WHERE user_id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return {}
        
        return {
            'weak_areas': json.loads(result[0]) if result[0] else [],
            'strong_areas': json.loads(result[1]) if result[1] else [],
            'total_tasks_completed': result[2],
            'avg_score': result[3],
            'recommended_topics': json.loads(result[4]) if result[4] else []
        }
    
    def get_recent_completions(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get recent task completions for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.id, t.title, t.concept, c.score, c.completed_at, c.concept_gaps
            FROM completions c
            JOIN tasks t ON c.task_id = t.id
            WHERE c.user_id = ?
            ORDER BY c.completed_at DESC
            LIMIT ?
        ''', (user_id, limit))
        
        completions = []
        for row in cursor.fetchall():
            completions.append({
                'id': row[0],
                'title': row[1],
                'concept': row[2],
                'score': row[3],
                'completed_at': row[4],
                'concept_gaps': json.loads(row[5]) if row[5] else []
            })
        
        conn.close()
        return completions
    
    def update_skill_level(self, user_id: int, skill_level: str):
        """Update user's detected skill level"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE users SET skill_level = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (skill_level, user_id)
        )
        conn.commit()
        conn.close()
    
    def get_user_skill_level(self, user_id: int) -> str:
        """Get user's current skill level"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT skill_level FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 'beginner'
