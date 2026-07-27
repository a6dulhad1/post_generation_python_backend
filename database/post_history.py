"""Database for tracking post history."""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from config.settings import settings
from loguru import logger


class PostHistory:
    """Track posted content to avoid duplicates and maintain history."""
    
    def __init__(self):
        self.db_path = settings.DATABASE_PATH
        self._init_database()
    
    def _init_database(self):
        """Initialize the database with required tables."""
        # Ensure directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                text TEXT NOT NULL,
                hashtags TEXT,
                image_path TEXT,
                platform TEXT NOT NULL,
                posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'posted',
                post_id TEXT,
                engagement_data TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS post_ideas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                angle TEXT,
                key_points TEXT,
                target_audience TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                used INTEGER DEFAULT 0
            )
        """)
        
        conn.commit()
        conn.close()
        
        logger.info(f"Database initialized at {self.db_path}")
    
    def add_post(self, post_data: dict) -> int:
        """
        Add a posted entry to history.
        
        Args:
            post_data: Dictionary with post information
            
        Returns:
            ID of the inserted record
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO posts (topic, text, hashtags, image_path, platform, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            post_data.get('topic', ''),
            post_data.get('text', ''),
            post_data.get('hashtags', ''),
            post_data.get('image_path', ''),
            post_data.get('platform', ''),
            post_data.get('status', 'posted')
        ))
        
        post_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Added post to history: ID {post_id}")
        return post_id
    
    def get_recent_posts(self, limit: int = 10, platform: str = None) -> list:
        """
        Get recent posts from history.
        
        Args:
            limit: Number of posts to retrieve
            platform: Optional platform filter
            
        Returns:
            List of post dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if platform:
            cursor.execute("""
                SELECT * FROM posts 
                WHERE platform = ?
                ORDER BY posted_at DESC 
                LIMIT ?
            """, (platform, limit))
        else:
            cursor.execute("""
                SELECT * FROM posts 
                ORDER BY posted_at DESC 
                LIMIT ?
            """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        posts = [dict(row) for row in rows]
        return posts
    
    def get_posts_by_date(self, date: str, platform: str = None) -> list:
        """
        Get posts for a specific date.
        
        Args:
            date: Date in YYYY-MM-DD format
            platform: Optional platform filter
            
        Returns:
            List of post dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if platform:
            cursor.execute("""
                SELECT * FROM posts 
                WHERE DATE(posted_at) = ? AND platform = ?
                ORDER BY posted_at DESC
            """, (date, platform))
        else:
            cursor.execute("""
                SELECT * FROM posts 
                WHERE DATE(posted_at) = ?
                ORDER BY posted_at DESC
            """, (date,))
        
        rows = cursor.fetchall()
        conn.close()
        
        posts = [dict(row) for row in rows]
        return posts
    
    def check_duplicate(self, text: str, days: int = 30) -> bool:
        """
        Check if similar content was posted recently.
        
        Args:
            text: Post text to check
            days: Number of days to look back
            
        Returns:
            True if duplicate found, False otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) FROM posts 
            WHERE text = ? 
            AND posted_at >= datetime('now', '-' || ? || ' days')
        """, (text, days))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count > 0
    
    def add_idea(self, idea: dict) -> int:
        """Save a post idea for future use."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO post_ideas (topic, angle, key_points, target_audience)
            VALUES (?, ?, ?, ?)
        """, (
            idea.get('topic', ''),
            idea.get('angle', ''),
            json.dumps(idea.get('key_points', [])),
            idea.get('target_audience', '')
        ))
        
        idea_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return idea_id
    
    def get_unused_ideas(self, limit: int = 5) -> list:
        """Get ideas that haven't been used yet."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM post_ideas 
            WHERE used = 0 
            ORDER BY created_at DESC 
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        ideas = []
        for row in rows:
            idea = dict(row)
            idea['key_points'] = json.loads(idea['key_points'])
            ideas.append(idea)
        
        return ideas
    
    def mark_idea_used(self, idea_id: int):
        """Mark an idea as used."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE post_ideas 
            SET used = 1 
            WHERE id = ?
        """, (idea_id,))
        
        conn.commit()
        conn.close()
    
    def get_stats(self) -> dict:
        """Get posting statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total posts
        cursor.execute("SELECT COUNT(*) FROM posts")
        total_posts = cursor.fetchone()[0]
        
        # Posts by platform
        cursor.execute("""
            SELECT platform, COUNT(*) as count 
            FROM posts 
            GROUP BY platform
        """)
        by_platform = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Posts this week
        cursor.execute("""
            SELECT COUNT(*) FROM posts 
            WHERE posted_at >= datetime('now', '-7 days')
        """)
        posts_this_week = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_posts": total_posts,
            "by_platform": by_platform,
            "posts_this_week": posts_this_week
        }
