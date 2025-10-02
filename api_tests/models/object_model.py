"""
Pydantic models for Object API.
"""
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, validator


class ObjectData(BaseModel):
    """Model for object data field."""
    year: Optional[int] = None
    price: Optional[float] = None
    cpu_model: Optional[str] = Field(None, alias="CPU model")
    hard_disk_size: Optional[str] = Field(None, alias="Hard disk size")
    color: Optional[str] = None
    generation: Optional[str] = None
    capacity: Optional[str] = None
    
    class Config:
        populate_by_name = True
        extra = "allow"  # Allow additional fields


class ObjectRequest(BaseModel):
    """Model for object creation/update request."""
    name: str
    data: Optional[Dict[str, Any]] = None
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Name must not be empty')
        return v


class ObjectResponse(BaseModel):
    """Model for object response."""
    id: str
    name: str
    data: Optional[Dict[str, Any]] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    
    class Config:
        extra = "allow"  # Allow additional fields


class DeleteResponse(BaseModel):
    """Model for delete operation response."""
    message: str
    
    class Config:
        extra = "allow"


