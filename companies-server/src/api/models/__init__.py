"""Companies House API models."""

from src.api.models.base import BaseAPIModel
from src.api.models.common import Address, SearchMatches, Links
from src.api.models.search import (
    # Company search (simple)
    CompanySearchParams,
    CompanySearchResponse,
    CompanySearchResult,
    # Advanced company search
    AdvancedSearchParams,
    AdvancedSearchResponse,
    AdvancedSearchResult,
    RegisteredOfficeAddress,
    # Officer search
    OfficerSearchParams,
    OfficerSearchResponse,
    OfficerSearchResult,
    DateOfBirth,
)

__all__ = [
    # Base
    "BaseAPIModel",
    # Common
    "Address",
    "SearchMatches",
    "Links",
    # Company search
    "CompanySearchParams",
    "CompanySearchResponse",
    "CompanySearchResult",
    # Advanced search
    "AdvancedSearchParams",
    "AdvancedSearchResponse",
    "AdvancedSearchResult",
    "RegisteredOfficeAddress",
    # Officer search
    "OfficerSearchParams",
    "OfficerSearchResponse",
    "OfficerSearchResult",
    "DateOfBirth",
]
