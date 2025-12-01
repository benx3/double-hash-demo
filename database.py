"""
Database manager for saving/loading hash table to/from JSON
"""
import json
import os
from typing import Optional
from double_hashing import DoubleHashTable


class DatabaseManager:
    """Manage persistence of hash table to JSON file"""
    
    def __init__(self, filepath: str = "products_db.json"):
        """
        Initialize database manager
        
        Args:
            filepath: Path to JSON database file
        """
        self.filepath = filepath
    
    def save(self, hash_table: DoubleHashTable) -> bool:
        """
        Save hash table to JSON file
        
        Args:
            hash_table: DoubleHashTable instance to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = hash_table.to_dict()
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving to database: {e}")
            return False
    
    def load(self) -> Optional[DoubleHashTable]:
        """
        Load hash table from JSON file
        
        Returns:
            DoubleHashTable instance if file exists, None otherwise
        """
        if not os.path.exists(self.filepath):
            return None
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return DoubleHashTable.from_dict(data)
        except Exception as e:
            print(f"Error loading from database: {e}")
            return None
    
    def exists(self) -> bool:
        """Check if database file exists"""
        return os.path.exists(self.filepath)
    
    def delete(self) -> bool:
        """Delete database file"""
        try:
            if self.exists():
                os.remove(self.filepath)
            return True
        except Exception as e:
            print(f"Error deleting database: {e}")
            return False
