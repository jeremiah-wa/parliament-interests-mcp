"""
Pydantic models for Parliament Interests API responses.

These models are based on the OpenAPI specification from:
https://interests-api.parliament.uk/swagger/v1/swagger.json
"""

from datetime import date
from enum import Enum
from typing import Any, Generic, TypeVar
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
    """Member of Parliament who has registered the interest"""

    house: str | None = pyd.Field(
        default=None,
        description="The name of the House the Member is currently associated with",
    )
    member_from: str | None = pyd.Field(
        default=None, alias="memberFrom", description="Constituency of Commons Members"
    )
    party: str | None = pyd.Field(
        default=None,
        description="Party the Member is currently associated with",
    )
    links: list[Link] | None = pyd.Field(
        default=None,
        description="A list of HATEOAS Links for retrieving further information about this member",
    )


class PublishedCategory(BaseAPIModel):
    """Category an interest can be registered with."""

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
    """Version of an interest which has been published."""

    id: int = pyd.Field(description="ID of the interest")
    summary: str | None = pyd.Field(
        default=None, description="Title Summary for the interest."
    )
    parent_interest_id: int | None = pyd.Field(
        default=None,
        alias="parentInterestId",
        description="The unique ID for the payer (parent interest) to which this payment (child interest) is associated.",
    )
    registration_date: date | None = pyd.Field(
        default=None,
        alias="registrationDate",
        description="Registration Date on the published interest.",
    )
    published_date: date | None = pyd.Field(
        default=None,
        alias="publishedDate",
        description="Date when the interest was first published.",
    )
    updated_dates: list[date] | None = pyd.Field(
        default=None,
        alias="updatedDates",
        description="A list of dates on which the interest has been updated since it has been published.",
    )

    # Related objects
    member: Member | None = pyd.Field(
        default=None, description="Member who registered the interest"
    )
    category: PublishedCategory | None = pyd.Field(
        default=None, description="Interest category"
    )
    published_register: PublishedRegister | None = pyd.Field(
        default=None, alias="register", description="Register"
    )
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

T = TypeVar("T", bound=BaseAPIModel)


class ApiLinkedSearchResult(BaseAPIModel, Generic[T]):
    """Paginated search result for published categories with HATEOAS links."""

    skip: int = pyd.Field(
        default=0, description="The skip value that was used in the query."
    )
    take: int = pyd.Field(
        default=20, description="The take value that was used in the query."
    )
    total_results: int = pyd.Field(
        default=0,
        alias="totalResults",
        description="The total number of results that matched the query.",
    )
    items: list[T] | None = pyd.Field(
        default=None,
        description="The list of items found for the specified page (by requested skip and take)",
    )
    links: list[Link] | None = pyd.Field(
        default=None,
        description="A list of HATEOAS Links for navigating through the paginated result.",
    )


class PublishedInterestApiLinkedSearchResult(ApiLinkedSearchResult[PublishedInterest]):
    """Paginated search result for published interests with HATEOAS links."""


class PublishedCategoryApiLinkedSearchResult(ApiLinkedSearchResult[PublishedCategory]):
    """Paginated search result for published categories with HATEOAS links."""


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
    expand_child_interests: bool = pyd.Field(
        default=True, description="Expand child interests", alias="ExpandChildInterests"
    )

    @pyd.field_serializer("expand_child_interests")
    def serialize_expand_child_interests(self, value: bool) -> str:
        """Convert boolean to lowercase string for HTTP query parameters."""
        return str(value).lower()
