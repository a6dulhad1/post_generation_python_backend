"""Database configuration and tables"""
import sqlalchemy
from databases import Database
from sqlalchemy import MetaData, Table, Column, String, Integer, DateTime, JSON, Boolean
from datetime import datetime

import os

# Ensure data directory exists
os.makedirs("./data", exist_ok=True)

# Database URL (SQLite for development, PostgreSQL/Environment for production)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

database = Database(DATABASE_URL)
metadata = MetaData()


# Users table
users_table = Table(
    "users",
    metadata,
    Column("id", String, primary_key=True),
    Column("email", String, unique=True, nullable=False),
    Column("name", String, nullable=False),
    Column("password_hash", String, nullable=False),
    Column("topics", JSON, default=[]),
    Column("posts_per_day", Integer, default=3),
    Column("platforms", JSON, default=[]),
    Column("linkedin_token", String, nullable=True),
    Column("facebook_token", String, nullable=True),
    Column("facebook_page_id", String, nullable=True),
    Column("instagram_account_id", String, nullable=True),
    Column("created_at", DateTime, default=datetime.utcnow),
)

# Posts table
posts_table = Table(
    "posts",
    metadata,
    Column("id", String, primary_key=True),
    Column("user_id", String, nullable=False),
    Column("text", String, nullable=False),
    Column("hashtags", String, nullable=True),
    Column("platforms", JSON, nullable=False),
    Column("image_path", String, nullable=True),
    Column("status", String, default="draft"),  # draft, scheduled, published
    Column("schedule_time", DateTime, nullable=True),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("published_at", DateTime, nullable=True),
)

# Chat sessions table
sessions_table = Table(
    "chat_sessions",
    metadata,
    Column("id", String, primary_key=True),
    Column("user_id", String, nullable=False),
    Column("conversation_id", String, nullable=False),
    Column("user_message", String, nullable=False),
    Column("ai_response", String, nullable=False),
    Column("created_at", DateTime, default=datetime.utcnow),
)

# Create tables
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = sqlalchemy.create_engine(DATABASE_URL, connect_args=connect_args)
metadata.create_all(engine)

