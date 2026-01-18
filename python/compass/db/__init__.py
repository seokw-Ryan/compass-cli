"""Database layer for Compass.

All database operations use local SQLite storage. The database file is
stored within the vault directory to ensure data remains local and portable.
"""

__all__ = ["schema", "migrate", "models", "manager", "DatabaseManager"]
