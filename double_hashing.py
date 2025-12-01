"""
Double Hashing implementation for Product Management
"""
from typing import Optional, List, Tuple, Dict
from models import Product, HashEntry


class CollisionLog:
    """Log entry for collision events"""
    def __init__(self, key: str, operation: str, probe_sequence: List[int], resolution: str, 
                 calculation_details: Dict = None):
        self.key = key
        self.operation = operation  # 'insert', 'search', 'delete'
        self.probe_sequence = probe_sequence
        self.resolution = resolution  # Description of how collision was resolved
        self.collision_count = len(probe_sequence) - 1  # Number of collisions
        self.calculation_details = calculation_details or {}  # Detailed math steps


class DoubleHashTable:
    """Hash table with Double Hashing collision resolution"""
    
    def __init__(self, size: int = 10):
        """
        Initialize hash table with given size
        
        Args:
            size: Size of hash table (should be prime number for better distribution)
        """
        self.size = size
        self.table: List[Optional[HashEntry]] = [None] * size
        self.count = 0  # Number of active elements
        self.collision_count = 0  # Track collisions for statistics
        self.collision_logs: List[CollisionLog] = []  # Detailed collision history
        
    def _hash1(self, key: str) -> int:
        """
        Primary hash function: sum of ASCII values mod table size
        
        Args:
            key: Product code string
            
        Returns:
            Hash value (0 to size-1)
        """
        hash_value = sum(ord(char) for char in key)
        return hash_value % self.size
    
    def _hash2(self, key: str) -> int:
        """
        Secondary hash function for double hashing
        Uses formula: R - (sum(ASCII) mod R) where R is largest prime < size
        
        Args:
            key: Product code string
            
        Returns:
            Step size for probing (1 to R)
        """
        R = self._get_prime_less_than(self.size)
        hash_value = sum(ord(char) for char in key)
        return R - (hash_value % R)
    
    def _get_prime_less_than(self, n: int) -> int:
        """
        Find largest prime number less than n
        
        Args:
            n: Upper bound
            
        Returns:
            Largest prime < n
        """
        def is_prime(num):
            if num < 2:
                return False
            for i in range(2, int(num ** 0.5) + 1):
                if num % i == 0:
                    return False
            return True
        
        for i in range(n - 1, 1, -1):
            if is_prime(i):
                return i
        return 1
    
    def _probe(self, key: str, i: int) -> int:
        """
        Calculate probe position using double hashing
        Formula: (hash1(key) + i * hash2(key)) mod size
        
        Args:
            key: Product code
            i: Probe attempt number (0, 1, 2, ...)
            
        Returns:
            Position in table
        """
        return (self._hash1(key) + i * self._hash2(key)) % self.size
    
    def insert(self, product: Product) -> Tuple[bool, str, List[int]]:
        """
        Insert product into hash table
        
        Args:
            product: Product to insert
            
        Returns:
            Tuple of (success, message, probe_sequence)
        """
        if self.count >= self.size:
            return False, "Hash table is full!", []
        
        key = product.ma_san_pham
        probe_sequence = []
        
        # Calculate detailed math for logging
        ascii_sum = sum(ord(char) for char in key)
        h1_value = self._hash1(key)
        h2_value = self._hash2(key)
        R = self._get_prime_less_than(self.size)
        
        calculation_details = {
            "key": key,
            "ascii_sum": ascii_sum,
            "ascii_breakdown": [(c, ord(c)) for c in key],
            "size": self.size,
            "R": R,
            "h1": h1_value,
            "h1_formula": f"{ascii_sum} mod {self.size} = {h1_value}",
            "h2": h2_value,
            "h2_formula": f"{R} - ({ascii_sum} mod {R}) = {R} - {ascii_sum % R} = {h2_value}",
            "probe_steps": []
        }
        
        for i in range(self.size):
            pos = self._probe(key, i)
            probe_sequence.append(pos)
            
            # Log detailed probe step
            probe_formula = f"({h1_value} + {i} × {h2_value}) mod {self.size} = ({h1_value} + {i * h2_value}) mod {self.size} = {pos}"
            step_info = {
                "attempt": i,
                "formula": probe_formula,
                "position": pos,
                "status": "occupied" if self.table[pos] and not self.table[pos].is_deleted else ("deleted" if self.table[pos] else "empty")
            }
            if self.table[pos] and not self.table[pos].is_deleted:
                step_info["occupied_by"] = self.table[pos].product.ma_san_pham
            calculation_details["probe_steps"].append(step_info)
            
            # Empty slot or deleted slot
            if self.table[pos] is None or self.table[pos].is_deleted:
                self.table[pos] = HashEntry(product, False)
                self.count += 1
                
                # Log collision if occurred
                if i > 0:
                    self.collision_count += 1
                    resolution = f"Giải quyết bằng Double Hashing sau {i} lần thăm dò. Vị trí cuối: {pos}"
                    self.collision_logs.append(CollisionLog(key, "INSERT", probe_sequence.copy(), resolution, calculation_details))
                
                return True, f"Inserted at position {pos}", probe_sequence
            
            # Key already exists
            if self.table[pos].product.ma_san_pham == key:
                return False, "Product code already exists!", probe_sequence
            
            # Collision occurred
            if i == 0:
                self.collision_count += 1
        
        return False, "Could not insert (table full)", probe_sequence
    
    def search(self, key: str) -> Tuple[Optional[Product], int, List[int]]:
        """
        Search for product by key
        
        Args:
            key: Product code
            
        Returns:
            Tuple of (product or None, position, probe_sequence)
        """
        probe_sequence = []
        
        # Calculate detailed math for logging
        ascii_sum = sum(ord(char) for char in key)
        h1_value = self._hash1(key)
        h2_value = self._hash2(key)
        R = self._get_prime_less_than(self.size)
        
        calculation_details = {
            "key": key,
            "ascii_sum": ascii_sum,
            "ascii_breakdown": [(c, ord(c)) for c in key],
            "size": self.size,
            "R": R,
            "h1": h1_value,
            "h1_formula": f"{ascii_sum} mod {self.size} = {h1_value}",
            "h2": h2_value,
            "h2_formula": f"{R} - ({ascii_sum} mod {R}) = {R} - {ascii_sum % R} = {h2_value}",
            "probe_steps": []
        }
        
        for i in range(self.size):
            pos = self._probe(key, i)
            probe_sequence.append(pos)
            
            # Log detailed probe step
            probe_formula = f"({h1_value} + {i} × {h2_value}) mod {self.size} = ({h1_value} + {i * h2_value}) mod {self.size} = {pos}"
            step_info = {
                "attempt": i,
                "formula": probe_formula,
                "position": pos,
                "status": "empty" if self.table[pos] is None else ("deleted" if self.table[pos].is_deleted else "occupied")
            }
            if self.table[pos] and not self.table[pos].is_deleted:
                step_info["found_key"] = self.table[pos].product.ma_san_pham
            calculation_details["probe_steps"].append(step_info)
            
            if self.table[pos] is None:
                if i > 0:
                    resolution = f"Tìm kiếm thất bại sau {i} lần thăm dò. Gặp slot trống tại vị trí {pos}"
                    self.collision_logs.append(CollisionLog(key, "SEARCH", probe_sequence.copy(), resolution, calculation_details))
                return None, -1, probe_sequence
            
            if not self.table[pos].is_deleted and self.table[pos].product.ma_san_pham == key:
                if i > 0:
                    resolution = f"Tìm thấy sau {i} lần thăm dò tại vị trí {pos}"
                    self.collision_logs.append(CollisionLog(key, "SEARCH", probe_sequence.copy(), resolution, calculation_details))
                return self.table[pos].product, pos, probe_sequence
        
        return None, -1, probe_sequence
    
    def delete(self, key: str) -> Tuple[bool, str, List[int]]:
        """
        Delete product by key (lazy deletion)
        
        Args:
            key: Product code
            
        Returns:
            Tuple of (success, message, probe_sequence)
        """
        product, pos, probe_sequence = self.search(key)
        
        if product is None:
            return False, "Product not found!", probe_sequence
        
        self.table[pos].is_deleted = True
        self.count -= 1
        return True, f"Deleted from position {pos}", probe_sequence
    
    def get_all_products(self) -> List[Tuple[int, Product]]:
        """
        Get all active products with their positions
        
        Returns:
            List of (position, product) tuples
        """
        products = []
        for i, entry in enumerate(self.table):
            if entry is not None and not entry.is_deleted:
                products.append((i, entry.product))
        return products
    
    def get_table_state(self) -> List[dict]:
        """
        Get full table state for visualization
        
        Returns:
            List of dictionaries representing each slot
        """
        state = []
        for i, entry in enumerate(self.table):
            if entry is None:
                state.append({"index": i, "status": "empty", "product": None})
            elif entry.is_deleted:
                state.append({"index": i, "status": "deleted", "product": entry.product.ma_san_pham})
            else:
                state.append({"index": i, "status": "occupied", "product": entry.product})
        return state
    
    def get_collision_logs(self) -> List[Dict]:
        """
        Get detailed collision logs
        
        Returns:
            List of collision log dictionaries
        """
        return [
            {
                "key": log.key,
                "operation": log.operation,
                "probe_sequence": log.probe_sequence,
                "collision_count": log.collision_count,
                "resolution": log.resolution,
                "calculation_details": log.calculation_details
            }
            for log in self.collision_logs
        ]
    
    def get_statistics(self) -> dict:
        """
        Get hash table statistics
        
        Returns:
            Dictionary with statistics
        """
        occupied = sum(1 for entry in self.table if entry and not entry.is_deleted)
        deleted = sum(1 for entry in self.table if entry and entry.is_deleted)
        empty = self.size - occupied - deleted
        load_factor = occupied / self.size if self.size > 0 else 0
        
        return {
            "size": self.size,
            "occupied": occupied,
            "deleted": deleted,
            "empty": empty,
            "load_factor": load_factor,
            "collisions": self.collision_count,
            "total_collision_events": len(self.collision_logs)
        }
    
    def to_dict(self) -> dict:
        """Convert hash table to dictionary for JSON serialization"""
        return {
            "size": self.size,
            "count": self.count,
            "collision_count": self.collision_count,
            "collision_logs": self.get_collision_logs(),
            "table": [entry.to_dict() if entry else None for entry in self.table]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'DoubleHashTable':
        """Create hash table from dictionary"""
        ht = cls(data["size"])
        ht.count = data["count"]
        ht.collision_count = data["collision_count"]
        ht.table = [
            HashEntry.from_dict(entry) if entry else None 
            for entry in data["table"]
        ]
        # Restore collision logs if available
        if "collision_logs" in data:
            ht.collision_logs = [
                CollisionLog(
                    log["key"],
                    log["operation"],
                    log["probe_sequence"],
                    log["resolution"],
                    log.get("calculation_details", {})
                )
                for log in data["collision_logs"]
            ]
        return ht
