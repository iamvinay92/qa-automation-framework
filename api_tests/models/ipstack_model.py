"""
Pydantic models for ipstack API request/response validation.

These models ensure type safety and automatic validation of API responses.
"""
from typing import Optional, List
from pydantic import BaseModel, Field, validator


class Language(BaseModel):
    """Language information model."""
    code: str
    name: str
    native: str


class Location(BaseModel):
    """Detailed location information model."""
    geoname_id: int
    capital: str
    languages: List[Language]
    country_flag: str
    country_flag_emoji: str
    country_flag_emoji_unicode: str
    calling_code: str
    is_eu: bool


class IpstackResponse(BaseModel):
    """
    Main response model for ipstack API.
    
    This model validates the structure and types of the API response.
    """
    ip: str
    type: str
    continent_code: Optional[str] = None
    continent_name: Optional[str] = None
    country_code: str
    country_name: str
    region_code: Optional[str] = None
    region_name: Optional[str] = None
    city: Optional[str] = None
    zip: Optional[str] = None
    latitude: float
    longitude: float
    msa: Optional[str] = None
    dma: Optional[str] = None
    radius: Optional[str] = None
    ip_routing_type: Optional[str] = None
    connection_type: Optional[str] = None
    location: Optional[Location] = None
    
    @validator('type')
    def validate_ip_type(cls, v):
        """Validate IP type is either ipv4 or ipv6."""
        if v not in ['ipv4', 'ipv6']:
            raise ValueError('IP type must be ipv4 or ipv6')
        return v
    
    @validator('latitude')
    def validate_latitude(cls, v):
        """Validate latitude is within valid range."""
        if not -90 <= v <= 90:
            raise ValueError('Latitude must be between -90 and 90')
        return v
    
    @validator('longitude')
    def validate_longitude(cls, v):
        """Validate longitude is within valid range."""
        if not -180 <= v <= 180:
            raise ValueError('Longitude must be between -180 and 180')
        return v


class IpstackErrorResponse(BaseModel):
    """Error response model for ipstack API."""
    success: bool = False
    error: dict
    
    class Config:
        """Pydantic config."""
        extra = "allow"


class SecurityInfo(BaseModel):
    """Security information model (available in paid plans)."""
    is_proxy: Optional[bool] = None
    proxy_type: Optional[str] = None
    is_crawler: Optional[bool] = None
    crawler_name: Optional[str] = None
    crawler_type: Optional[str] = None
    is_tor: Optional[bool] = None
    threat_level: Optional[str] = None
    threat_types: Optional[List[str]] = None


