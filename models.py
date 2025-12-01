"""
Models for Product Management System using Double Hashing
"""
from dataclasses import dataclass, asdict
from typing import Optional
import json


@dataclass
class Product:
    """Product model with basic attributes"""
    ma_san_pham: str  # Product code (Primary Key)
    ten_san_pham: str  # Product name
    gia: float  # Price
    so_luong: int  # Quantity
    mo_ta: str = ""  # Description (optional)
    
    def to_dict(self) -> dict:
        """Convert product to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Product':
        """Create product from dictionary"""
        return cls(**data)
    
    def __str__(self) -> str:
        """String representation of product"""
        return f"[{self.ma_san_pham}] {self.ten_san_pham} - {self.gia:,.0f}đ (SL: {self.so_luong})"
    
    def to_display_dict(self) -> dict:
        """Convert to dictionary for display"""
        return {
            "Mã SP": self.ma_san_pham,
            "Tên sản phẩm": self.ten_san_pham,
            "Giá": f"{self.gia:,.0f}đ",
            "Số lượng": self.so_luong,
            "Mô tả": self.mo_ta
        }


class HashEntry:
    """Entry in hash table with deletion flag"""
    def __init__(self, product: Product, is_deleted: bool = False):
        self.product = product
        self.is_deleted = is_deleted
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "product": self.product.to_dict() if self.product else None,
            "is_deleted": self.is_deleted
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'HashEntry':
        """Create from dictionary"""
        product = Product.from_dict(data["product"]) if data.get("product") else None
        return cls(product, data.get("is_deleted", False))
