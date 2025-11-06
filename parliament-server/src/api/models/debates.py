"""
Pydantic models for Parliament Hansard API responses.

These models are based on the OpenAPI specification from:
https://hansard-api.parliament.uk/swagger/docs/v1
"""

from datetime import datetime
from pydantic import Field, field_validator
from enum import Enum
from typing import Literal

from .base import BaseAPIModel

class Source(int, Enum):
    ROLLING_HANSARD = 1
    DAILY_HANSARD = 2
    BOUND_VOLUME = 3
    HISTORIC = 4


class DebateOverview(BaseAPIModel):
    """Overview information for a debate."""

    id: int  = Field(alias="Id", description="Debate ID")
    ext_id: str = Field(alias="ExtId", description="External ID")
    title: str = Field(alias="Title", description="Debate title")
    hrs_tag: str = Field(alias="HRSTag", description="HRS tag")
    date: datetime = Field(alias="Date", description="Debate date")
    location: str = Field(alias="Location", description="Location")
    house: str = Field(alias="House", description="House (Commons/Lords)")
    source: Source = Field(alias="Source", description="Source of the debate")
    volume_no: int | None = Field(
        default=None, alias="VolumeNo", description="Volume number"
    )
    content_last_updated: datetime | None = Field(
        default=None, alias="ContentLastUpdated", description="Last update timestamp"
    )
    debate_type_id: int | None = Field(
        default=None, alias="DebateTypeId", description="Debate type ID"
    )
    section_type: int | None = Field(
        default=None, alias="SectionType", description="Section type"
    )
    next_debate_ext_id: str | None = Field(
        default=None, alias="NextDebateExtId", description="Next debate external ID"
    )
    next_debate_title: str | None = Field(
        default=None, alias="NextDebateTitle", description="Next debate title"
    )
    previous_debate_ext_id: str | None = Field(
        default=None,
        alias="PreviousDebateExtId",
        description="Previous debate external ID",
    )
    previous_debate_title: str | None = Field(
        default=None, alias="PreviousDebateTitle", description="Previous debate title"
    )

    @field_validator("date", "content_last_updated", mode="before")
    @classmethod
    def parse_date_string(cls, value):
        """Convert date-only strings to datetime format."""
        if value is None:
            return None
        if isinstance(value, str):
            # If the string is just a date (YYYY-MM-DD), append time component
            if len(value) == 10 and value.count("-") == 2:
                return f"{value}T00:00:00"
        return value


class SectionTreeItem(BaseAPIModel):
    """Navigation tree item for debate sections."""

    id: int | None = Field(default=None, alias="Id", description="Section ID")
    title: str | None = Field(default=None, alias="Title", description="Section title")
    parent_id: int | None = Field(
        default=None, alias="ParentId", description="Parent section ID"
    )
    sort_order: int | None = Field(
        default=None, alias="SortOrder", description="Sort order"
    )
    external_id: str | None = Field(
        default=None, alias="ExternalId", description="External ID"
    )
    hrs_tag: str | None = Field(default=None, alias="HRSTag", description="HRS tag")
    hansard_section: str | None = Field(
        default=None, alias="HansardSection", description="Hansard section"
    )
    timecode: datetime | None = Field(
        default=None, alias="Timecode", description="Timecode"
    )


class DebateItem(BaseAPIModel):
    """Individual item within a debate (speech, intervention, etc.)."""

    item_type: str | None = Field(
        default=None, alias="ItemType", description="Type of item"
    )
    item_id: int | None = Field(default=None, alias="ItemId", description="Item ID")
    member_id: int | None = Field(
        default=None, alias="MemberId", description="Member ID"
    )
    attributed_to: str | None = Field(
        default=None, alias="AttributedTo", description="Attribution"
    )
    value: str | None = Field(default=None, alias="Value", description="Content value")
    order_in_section: int | None = Field(
        default=None, alias="OrderInSection", description="Order within section"
    )
    timecode: datetime | None = Field(
        default=None, alias="Timecode", description="Timecode"
    )
    external_id: str | None = Field(
        default=None, alias="ExternalId", description="External ID"
    )
    hrs_tag: str | None = Field(default=None, alias="HRSTag", description="HRS tag")
    hansard_section: str | None = Field(
        default=None, alias="HansardSection", description="Hansard section"
    )
    uin: str | None = Field(
        default=None, alias="UIN", description="Unique identification number"
    )
    is_reiteration: bool | None = Field(
        default=None, alias="IsReiteration", description="Whether this is a reiteration"
    )

    @field_validator("timecode", mode="before")
    @classmethod
    def parse_date_string(cls, value):
        """Convert date-only strings to datetime format."""
        if value is None:
            return None
        if isinstance(value, str):
            # If the string is just a date (YYYY-MM-DD), append time component
            if len(value) == 10 and value.count("-") == 2:
                return f"{value}T00:00:00"
        return value


class Debate(BaseAPIModel):
    """Complete debate record with overview, navigation, and items."""

    overview: DebateOverview | None = Field(
        default=None, alias="Overview", description="Overview of the debate"
    )
    navigator: list[SectionTreeItem] = Field(
        default_factory=list, alias="Navigator", description="Navigation tree"
    )
    items: list[DebateItem] = Field(
        default_factory=list, alias="Items", description="Debate items"
    )
    child_debates: list["Debate"] = Field(
        default_factory=list, alias="ChildDebates", description="Child debates"
    )

class DebateResponse(BaseAPIModel):
    """Debate response for MCP tools (non-recursive version)."""
    debate: Debate | None = Field(default=None, alias="Debate", description="Debate")
