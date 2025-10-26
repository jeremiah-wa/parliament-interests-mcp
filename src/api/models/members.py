"""
Pydantic models for Parliament Members API responses.

These models are based on the OpenAPI specification from:
https://members-api.parliament.uk/swagger/v1/swagger.json
"""

from datetime import datetime
from enum import Enum

from pydantic import Field

from .base import BaseAPIModel, Link, BaseMember, BaseParams


class House(int, Enum):
    """House enumeration."""

    COMMONS = 1
    LORDS = 2


class MemberStatus(int, Enum):
    """Member status enumeration."""

    ACTIVE = 0
    INACTIVE = 1
    SUSPENDED = 2
    DECEASED = 3


class Status(int, Enum):
    """Status enumeration."""

    FLAG_0 = 0
    FLAG_1 = 1
    FLAG_2 = 2
    FLAG_3 = 3


class GovernmentType(int, Enum):
    """Government type enumeration."""

    TYPE_0 = 0
    TYPE_1 = 1
    TYPE_2 = 2
    TYPE_3 = 3


class MatchedBy(int, Enum):
    """Match type enumeration for search results.

    Note: These values are bit flags (powers of 2) that can be combined.
    The actual meaning of each flag is not documented in the official API.
    """

    FLAG_0 = 0
    FLAG_1 = 1
    FLAG_2 = 2
    FLAG_4 = 4
    FLAG_8 = 8
    FLAG_16 = 16
    FLAG_32 = 32
    FLAG_64 = 64
    FLAG_128 = 128
    FLAG_256 = 256
    FLAG_512 = 512
    FLAG_1024 = 1024
    FLAG_2048 = 2048
    FLAG_4096 = 4096
    FLAG_8192 = 8192


class Party(BaseAPIModel):
    id: int = Field(description="ID of the party")
    name: str | None = Field(default=None, description="Name of the party")
    abbreviation: str | None = Field(default=None, description="Party abbreviation")
    background_colour: str | None = Field(
        default=None,
        alias="backgroundColour",
        description="Background color for the party",
    )
    foreground_colour: str | None = Field(
        default=None,
        alias="foregroundColour",
        description="Foreground color for the party",
    )
    is_lords_main_party: bool = Field(
        default=False,
        alias="isLordsMainParty",
        description="Whether this is a main Lords party",
    )
    is_lords_spiritual_party: bool = Field(
        default=False,
        alias="isLordsSpiritualParty",
        description="Whether this is a Lords spiritual party",
    )
    government_type: GovernmentType | None = Field(
        default=None, alias="governmentType", description="Government type"
    )
    is_independent_party: bool = Field(
        default=False,
        alias="isIndependentParty",
        description="Whether this is an independent party",
    )


class MembershipStatus(BaseAPIModel):
    status_is_active: bool = Field(default=False, alias="statusIsActive")
    status_description: str | None = Field(default=None, alias="statusDescription")
    status_notes: str | None = Field(default=None, alias="statusNotes")
    status_id: int = Field(default=0, alias="statusId")
    status: int | None = Field(default=None, description="Status of the member")
    status_start_date: datetime | None = Field(
        default=None, alias="statusStartDate", description="Start date of the status"
    )


class HouseMembership(BaseAPIModel):
    """House membership information from Members API."""

    membership_from: str | None = Field(
        default=None, alias="membershipFrom", description="Membership from description"
    )
    membership_from_id: int | None = Field(
        default=None, alias="membershipFromId", description="Membership from ID"
    )
    house: House | None = Field(
        default=None, description="House of the member (1 for Commons, 2 for Lords)"
    )
    membership_start_date: datetime | None = Field(
        default=None,
        alias="membershipStartDate",
        description="Start date of membership",
    )
    membership_end_date: datetime | None = Field(
        default=None, alias="membershipEndDate", description="End date of membership"
    )
    membership_end_reason: str | None = Field(
        default=None,
        alias="membershipEndReason",
        description="End reason of membership",
    )
    membership_end_reason_id: int | None = Field(
        default=None,
        alias="membershipEndReasonId",
        description="End reason ID of membership",
    )
    membership_end_reason_notes: str | None = Field(
        default=None,
        alias="membershipEndReasonNotes",
        description="End reason notes of membership",
    )
    membership_status: MembershipStatus | None = Field(
        default=None, alias="membershipStatus", description="Membership status"
    )


class Member(BaseMember):
    """Member model from Members API."""

    latest_party: Party | None = Field(
        default=None, alias="latestParty", description="Latest party affiliation"
    )
    gender: str | None = Field(default=None, description="Gender of the member")
    latest_house_membership: HouseMembership | None = Field(
        default=None,
        alias="latestHouseMembership",
        description="Latest house membership",
    )
    thumbnail_url: str | None = Field(
        default=None,
        alias="thumbnailUrl",
        description="URL to member's thumbnail image",
    )


class MemberItem(BaseAPIModel):
    """Wrapper for member data."""

    value: Member | None = Field(default=None, description="Member data")
    links: list[Link] | None = Field(
        default=None, description="Links to related resources"
    )


class MemberMembersServiceSearchResult(BaseAPIModel):
    """Search result for members from Members API."""

    items: list[MemberItem] | None = Field(default=None, description="List of members")
    total_results: int = Field(
        default=0, alias="totalResults", description="Total results"
    )
    result_context: str | None = Field(
        default=None, alias="resultContext", description="Result context"
    )
    skip: int = Field(default=0, description="Skip value")
    take: int = Field(default=20, description="Take value")
    links: list[Link] | None = Field(
        default=None, description="Links to related resources"
    )
    result_type: MatchedBy | None = Field(
        default=None, alias="resultType", description="How the results were matched"
    )


class MemberSearchParams(BaseParams):
    name: str | None = Field(
        default=None, description="Members where name contains term specified"
    )
    location: str | None = Field(
        default=None,
        alias="Location",
        description="""Members where postcode or geographical location matches the term specified\r\n
        Searches for current constituencies with full postcode, or outward code; and name of constituency\r\n
        If there are no results based on above, searches for all current and past constituencies in specified area of UK.\r\n
        To explicitly search by area (ignoring name of constituency); please prefix query with `region:`.""",
    )
    post_title: str | None = Field(
        default=None,
        alias="PostTitle",
        description="Members which have held the post specified",
    )
    party_id: int | None = Field(
        default=None,
        description="Members which are currently affiliated with party with party ID",
    )
    house: House | None = Field(
        default=None,
        description="Members where their most recent house is the house specified",
    )
    constituency_id: int | None = Field(
        default=None,
        description="Members which currently hold the constituency with constituency id",
    )
    name_starts_with: str | None = Field(
        default=None,
        description="Members with surname begining with letter(s) specified",
    )
    gender: str | None = Field(
        default=None, alias="Gender", description="Members with the gender specified"
    )
    membership_started_since: datetime | None = Field(
        default=None,
        alias="MembershipStartedSince",
        description="Members who started on or after the date given",
    )
    membership_ended_since: datetime | None = Field(
        default=None,
        alias="MembershipEnded.MembershipEndedSince",
        description="Members who left the House on or after the date given",
    )
    membership_end_reason_ids: list[int] | None = Field(
        default=None,
        alias="MembershipEnded.MembershipEndReasonIds",
        description="Membership end reason IDs",
    )
    was_member_on_or_after: datetime | None = Field(
        default=None,
        alias="MembershipInDateRange.WasMemberOnOrAfter",
        description="Members who were active on or after the date specified",
    )
    was_member_on_or_before: datetime | None = Field(
        default=None,
        alias="MembershipInDateRange.WasMemberOnOrBefore",
        description="Members who were active on or before the date specified",
    )
    was_member_of_house: House | None = Field(
        default=None,
        alias="MembershipInDateRange.WasMemberOfHouse",
        description="Members who were active in the house specified",
    )
    is_eligible: bool | None = Field(
        default=None,
        alias="IsEligible",
        description="Members currently Eligible to sit in their House",
    )
    is_current_member: bool | None = Field(
        default=None,
        alias="IsCurrentMember",
        description="Members currently active in their House",
    )
    policy_interest_id: int | None = Field(
        default=None,
        alias="PolicyInterestId",
        description="Members with specified policy interest",
    )
    experience: str | None = Field(
        default=None,
        alias="Experience",
        description="Members with specified experience",
    )
