"""Search models for Companies House API.

This module contains all search-related models:
- Company search (simple and advanced)
- Officer search
"""

from datetime import date
from pydantic import Field
from src.api.models.base import BaseAPIModel
from src.api.models.common import Address, SearchMatches, Links


# ============================================================================
# COMPANY SEARCH (Simple - /search/companies)
# ============================================================================

class CompanySearchParams(BaseAPIModel):
    """Parameters for simple company search endpoint."""
    
    q: str = Field(description="Search term (company name or number)")
    items_per_page: int = Field(default=20, ge=1, le=100, description="Number of results per page")
    start_index: int = Field(default=0, ge=0, description="Starting index for pagination")
    restrictions: str | None = Field(None, description="Space-separated restrictions (e.g. 'active-companies')")


class CompanySearchResult(BaseAPIModel):
    """Individual company search result from simple search."""
    
    address: Address | None = Field(None, description="Company address")
    address_snippet: str | None = Field(None, description="Single line address with match highlighting")
    company_number: str | None = Field(None, description="Company registration number")
    company_status: str | None = Field(None, description="Company status (e.g., active, dissolved)")
    company_type: str | None = Field(None, description="Company type (e.g., ltd, plc)")
    date_of_cessation: date | None = Field(None, description="Date company was dissolved")
    date_of_creation: date | None = Field(None, description="Date company was incorporated")
    description: str | None = Field(None, description="Human-readable company description")
    description_identifier: list[str | None] | None = Field(None, description="Description type identifiers")
    kind: str | None = Field(None, description="Resource type (searchresults#company)")
    links: Links | None = Field(None, description="Links to related resources")
    matches: SearchMatches | None = Field(None, description="Character positions of search term matches")
    snippet: str | None = Field(None, description="Text snippet showing search context")
    title: str | None = Field(None, description="Company name")


class CompanySearchResponse(BaseAPIModel):
    """Response from /search/companies endpoint."""
    
    etag: str | None = Field(None, description="ETag of the resource")
    items: list[CompanySearchResult] = Field(default_factory=list, description="List of company search results")
    items_per_page: int = Field(description="Number of results per page")
    kind: str | None = Field(None, description="Resource type (search#companies)")
    start_index: int = Field(description="Starting index of results")
    total_results: int = Field(description="Total number of matching companies")


# ============================================================================
# ADVANCED COMPANY SEARCH (/advanced-search/companies)
# ============================================================================

class AdvancedSearchParams(BaseAPIModel):
    """Parameters for advanced company search with detailed filters."""
    
    company_name_includes: str | None = Field(None, description="Company name must include this term")
    company_name_excludes: str | None = Field(None, description="Company name must not include this term")
    company_status: list[str] | None = Field(None, description="Filter by company status (active, dissolved, etc.)")
    company_subtype: list[str] | None = Field(None, description="Filter by company subtype")
    company_type: list[str] | None = Field(None, description="Filter by company type (ltd, plc, llp, etc.)")
    dissolved_from: date | None = Field(None, description="Dissolved on or after this date")
    dissolved_to: date | None = Field(None, description="Dissolved on or before this date")
    incorporated_from: date | None = Field(None, description="Incorporated on or after this date")
    incorporated_to: date | None = Field(None, description="Incorporated on or before this date")
    location: str | None = Field(None, description="Filter by registered office location")
    sic_codes: list[str] | None = Field(None, description="Filter by SIC (industry) codes")
    size: int = Field(default=20, ge=1, le=5000, description="Number of results per page")
    start_index: int = Field(default=0, ge=0, description="Starting index for pagination")


class RegisteredOfficeAddress(BaseAPIModel):
    """Registered office address for advanced search results."""
    
    address_line_1: str | None = Field(None, description="First line of the address")
    address_line_2: str | None = Field(None, description="Second line of the address")
    country: str | None = Field(None, description="Country")
    locality: str | None = Field(None, description="Town or city")
    po_box: str | None = Field(None, description="Post office box number")
    postal_code: str | None = Field(None, description="Postal code")
    region: str | None = Field(None, description="Region or county")


class AdvancedSearchResult(BaseAPIModel):
    """Individual company result from advanced search."""
    
    company_name: str | None = Field(None, description="Company name")
    company_number: str | None = Field(None, description="Company registration number")
    company_status: str | None = Field(None, description="Company status (e.g., active, dissolved)")
    company_type: str | None = Field(None, description="Company type (e.g., ltd, plc)")
    date_of_cessation: date | None = Field(None, description="Date company was dissolved")
    date_of_creation: date | None = Field(None, description="Date company was incorporated")
    kind: str | None = Field(None, description="Resource type")
    registered_office_address: RegisteredOfficeAddress | None = Field(None, description="Registered office address")
    sic_codes: list[str] | None = Field(None, description="SIC (industry) codes")


class AdvancedSearchResponse(BaseAPIModel):
    """Response from /advanced-search/companies endpoint."""
    
    etag: str | None = Field(None, description="ETag of the resource")
    hits: int | None = Field(None, description="Total number of matching companies")
    items: list[AdvancedSearchResult] = Field(default_factory=list, description="List of company search results")
    kind: str | None = Field(None, description="Resource type")
    top_hit: AdvancedSearchResult | None = Field(None, description="Best matching result")


# ============================================================================
# OFFICER SEARCH (/search/officers)
# ============================================================================

class OfficerSearchParams(BaseAPIModel):
    """Parameters for officer search endpoint."""
    
    q: str = Field(description="Search term (officer name)")
    items_per_page: int = Field(default=20, ge=1, le=100, description="Number of results per page")
    start_index: int = Field(default=0, ge=0, description="Starting index for pagination")


class DateOfBirth(BaseAPIModel):
    """Partial date of birth for privacy (month and year only)."""
    
    month: int = Field(ge=1, le=12, description="Month of birth")
    year: int = Field(description="Year of birth")


class OfficerSearchResult(BaseAPIModel):
    """Individual officer search result."""
    
    address: Address | None = Field(None, description="Officer's service address")
    address_snippet: str | None = Field(None, description="Single line address with match highlighting")
    appointment_count: int | None = Field(None, description="Total number of company appointments")
    date_of_birth: DateOfBirth | None = Field(None, description="Partial date of birth (month and year)")
    description: str | None = Field(None, description="Human-readable officer description")
    description_identifiers: list[str | None] | None = Field(None, description="Description type identifiers (e.g., appointment-count, born-on)")
    kind: str | None = Field(None, description="Resource type (searchresults#officer)")
    links: Links | None = Field(None, description="Links to related resources")
    matches: SearchMatches | None = Field(None, description="Character positions of search term matches")
    snippet: str | None = Field(None, description="Text snippet showing search context")
    title: str | None = Field(None, description="Officer name")


class OfficerSearchResponse(BaseAPIModel):
    """Response from /search/officers endpoint."""
    
    etag: str | None = Field(None, description="ETag of the resource")
    items: list[OfficerSearchResult] = Field(default_factory=list, description="List of officer search results")
    items_per_page: int = Field(description="Number of results per page")
    kind: str | None = Field(None, description="Resource type (search#officers)")
    start_index: int = Field(description="Starting index of results")
    total_results: int = Field(description="Total number of matching officers")
