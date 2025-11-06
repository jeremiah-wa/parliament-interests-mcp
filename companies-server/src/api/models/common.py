"""Common models shared across Companies House API endpoints."""

from pydantic import Field
from src.api.models.base import BaseAPIModel


class Address(BaseAPIModel):
    """Standard address format used across Companies House APIs."""
    
    address_line_1: str | None = Field(None, description="First line of the address")
    address_line_2: str | None = Field(None, description="Second line of the address")
    care_of: str | None = Field(None, description="Care of name")
    country: str | None = Field(None, description="Country (e.g., UK)")
    locality: str | None = Field(None, description="Town or city")
    po_box: str | None = Field(None, description="Post office box number")
    postal_code: str | None = Field(None, description="Postal code (e.g., CF14 3UZ)")
    premises: str | None = Field(None, description="Property name or number")
    region: str | None = Field(None, description="Region or county")


class SearchMatches(BaseAPIModel):
    """Character positions for highlighting matched search terms.
    
    Positions are provided as pairs of integers defining start and end
    of substrings that matched the search terms.
    """
    
    address_snippet: list[int] | None = Field(None, description="Character offsets for matches in address_snippet")
    snippet: list[int] | None = Field(None, description="Character offsets for matches in snippet")
    title: list[int] | None = Field(None, description="Character offsets for matches in title")


class Links(BaseAPIModel):
    """Standard links object for API resources."""
    
    self: str = Field(description="URL to the resource")
