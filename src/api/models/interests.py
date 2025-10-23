"""
Pydantic models for Parliament Interests API responses.

These models are based on the OpenAPI specification from:
https://interests-api.parliament.uk/swagger/v1/swagger.json
"""

from datetime import date
from enum import Enum
from typing import Any
import pydantic as pyd

from .base import BaseAPIModel, BaseMember, Link, BaseParams


class RegisterType(str, Enum):
    """Register type for categories."""

    COMMONS = "Commons"
    LORDS = "Lords"


class InterestsSortOrder(str, Enum):
    """Sort order options for interests endpoints."""

    PUBLISHING_DATE_DESCENDING = "PublishingDateDescending"
    CATEGORY_ASCENDING = "CategoryAscending"


class FieldTypeInfo(BaseAPIModel):
    """Field type information model for interest fields from Interests API."""

    currency_code: str | None = pyd.Field(
        default=None, alias="currencyCode", description="Currency code of the field"
    )


class Field(BaseAPIModel):
    """Field model for interest fields from Interests API."""

    name: str | None = pyd.Field(default=None, description="Name of the field")
    description: str | None = pyd.Field(
        default=None, description="Description of the field"
    )
    type: str | None = pyd.Field(default=None, description="Type of the field")
    type_info: FieldTypeInfo | None = pyd.Field(
        default=None, alias="typeInfo", description="Type information of the field"
    )
    value: Any | None = pyd.Field(default=None, description="Value of the field")
    values: list[list["Field"]] | None = pyd.Field(
        default=None, description="Values of the field"
    )


class Member(BaseMember):
    """Member model for interests from Interests API."""

    house: str | None = pyd.Field(
        default=None,
        description="The name of the House the Member is currently associated with",
    )
    member_from: str | None = pyd.Field(
        default=None, alias="memberFrom", description="Constituency of Commons Members"
    )
    party: str | None = pyd.Field(
        default=None,
        description="Party the Member is currently associated with (simple string)",
    )
    links: list[Link] | None = pyd.Field(
        default=None,
        description="A list of HATEOAS Links for retrieving further information about this member",
    )


class PublishedCategory(BaseAPIModel):
    """Published category from Interests API."""

    id: int = pyd.Field(description="ID of the category")
    number: str | None = pyd.Field(
        default=None, description="Number of the category in the code of conduct."
    )
    name: str | None = pyd.Field(default=None, description="Name of the category")
    parent_category_ids: list[int] | None = pyd.Field(
        default=None,
        alias="parentCategoryIds",
        description="The unique ID for any parent category to which this category is associated, if the category is associated with another category",
    )
    type: RegisterType | None = pyd.Field(
        default=None,
        alias="registerType",
        description="The type of register of interests",
    )
    links: list[Link] | None = pyd.Field(
        default=None,
        description="A list of HATEOAS Links for retrieving related information about this register",
    )


class PublishedRegister(BaseAPIModel):
    """Published register from Interests API."""

    id: int = pyd.Field(description="ID of the register")
    published_date: str | None = pyd.Field(
        default=None,
        alias="publishedDate",
        description="Date when the Register was published.",
    )
    type: RegisterType | None = pyd.Field(
        default=None, description="The type of register of interests"
    )
    links: list[Link] | None = pyd.Field(
        default=None,
        description="A list of HATEOAS Links for retrieving related information about this register",
    )


class PublishedInterest(BaseAPIModel):
    """Published interest from Interests API."""

    id: int = pyd.Field(description="ID of the interest")
    summary: str | None = pyd.Field(default=None, description="Summary of the interest")
    parent_interest_id: int | None = pyd.Field(
        default=None, alias="parentInterestId", description="Parent interest ID"
    )
    registration_date: date | None = pyd.Field(
        default=None, alias="registrationDate", description="Registration date"
    )
    published_date: date | None = pyd.Field(
        default=None, alias="publishedDate", description="Published date"
    )
    updated_dates: list[date] | None = pyd.Field(
        default=None, alias="updatedDates", description="Updated dates"
    )

    # Related objects
    member: Member | None = pyd.Field(
        default=None, description="Member who registered the interest"
    )
    category: PublishedCategory | None = pyd.Field(
        default=None, description="Interest category"
    )
    register: PublishedRegister | None = pyd.Field(default=None, description="Register")
    fields: list[Field] | None = pyd.Field(default=None, description="Interest fields")
    child_interests: list["PublishedInterest"] | None = pyd.Field(
        default=None, alias="childInterests", description="Child interests"
    )
    links: list[Link] | None = pyd.Field(default=None, description="HATEOAS links")

    # Flags
    rectified: bool = pyd.Field(
        default=False, description="Whether the interest has been rectified"
    )
    rectified_details: str | None = pyd.Field(
        default=None, alias="rectifiedDetails", description="Rectification details"
    )


# Search Result Models
class PublishedInterestApiLinkedSearchResult(BaseAPIModel):
    """Search result for published interests from Interests API."""

    skip: int = pyd.Field(default=0, description="Skip value")
    take: int = pyd.Field(default=20, description="Take value")
    total_results: int = pyd.Field(
        default=0, alias="totalResults", description="Total results"
    )
    items: list[PublishedInterest] | None = pyd.Field(
        default=None, description="List of interests"
    )
    links: list[Link] | None = pyd.Field(
        default=None, description="Links to related resources"
    )


class ApiResponseErrorType(str, Enum):
    VALIDATION_ERROR = "ValidationError"
    AUTHENTICATION_ERROR = "AuthenticationError"
    CONNECTIVITY_ERROR = "ConnectivityError"
    GENERAL_ERROR = "GeneralError"


class ApiResponseError(BaseAPIModel):
    error_type: ApiResponseErrorType = pyd.Field(
        default=None, alias="errorType", description="Error type"
    )
    error_message: list[str] | None = pyd.Field(
        default=None, alias="errorMessage", description="Error message"
    )


class ObjectApiResponse(BaseAPIModel):
    """Object API response model."""

    error: ApiResponseError | None = pyd.Field(default=None, description="Error object")
    response: Any | None = pyd.Field(default=None, description="Response object")


class InterestsParams(BaseParams):
    member_id: int | None = pyd.Field(
        default=None, description="Filter by member ID", alias="MemberId"
    )
    category_id: int | None = pyd.Field(
        default=None, description="Filter by category ID", alias="CategoryId"
    )
    published_from: date | None = pyd.Field(
        default=None, description="Filter by published date from", alias="PublishedFrom"
    )
    published_to: date | None = pyd.Field(
        default=None, description="Filter by published date to", alias="PublishedTo"
    )
    sort_order: InterestsSortOrder | None = pyd.Field(
        default=None, description="Sort order for results", alias="SortOrder"
    )
    expand_child_interests: bool | None = pyd.Field(
        default=True, description="Expand child interests", alias="ExpandChildInterests"
    )

    @pyd.field_serializer("expand_child_interests")
    def serialize_expand_child_interests(self, value: bool | None) -> str | None:
        """Convert boolean to lowercase string for HTTP query parameters."""
        return str(value).lower() if value is not None else None
