"""
Pydantic models for Parliament Members API responses.

These models are based on the OpenAPI specification from:
https://members-api.parliament.uk/swagger/v1/swagger.json
"""

from datetime import datetime
from enum import Enum
from typing import TypeVar, Generic
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

    name_full_title: str | None = Field(
        default=None, alias="nameFullTitle", description="Member's full title"
    )
    name_address_as: str | None = Field(
        default=None, alias="nameAddressAs", description="Member's name for addressing"
    )
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


class DebateContribution(BaseAPIModel):
    """Debate contribution model from Members API."""

    total_contributions: int = Field(
        default=0,
        alias="totalContributions",
        description="Total number of contributions",
    )
    debate_title: str | None = Field(
        default=None, alias="debateTitle", description="Title of the debate"
    )
    debate_id: int = Field(default=0, alias="debateId", description="ID of the debate")
    debate_website_id: str | None = Field(
        default=None, alias="debateWebsiteId", description="Website ID of the debate"
    )
    sitting_date: datetime = Field(
        alias="sittingDate", description="Date of the sitting"
    )
    section: str | None = Field(default=None, description="Section of the debate")
    house: str | None = Field(default=None, description="House where debate occurred")
    first_timecode: datetime | None = Field(
        default=None,
        alias="firstTimecode",
        description="Timecode of first contribution",
    )
    speech_count: int = Field(
        default=0, alias="speechCount", description="Number of speeches"
    )
    question_count: int = Field(
        default=0, alias="questionCount", description="Number of questions"
    )
    supplementary_question_count: int = Field(
        default=0,
        alias="supplementaryQuestionCount",
        description="Number of supplementary questions",
    )
    intervention_count: int = Field(
        default=0, alias="interventionCount", description="Number of interventions"
    )
    answer_count: int = Field(
        default=0, alias="answerCount", description="Number of answers"
    )
    points_of_order_count: int = Field(
        default=0, alias="pointsOfOrderCount", description="Number of points of order"
    )
    statements_count: int = Field(
        default=0, alias="statementsCount", description="Number of statements"
    )

class RegisteredInterest(BaseAPIModel):
    """Interest model from Members API."""
    id: int = Field(default=0, description="ID of the interest")
    interest: str | None = Field(default=None, description="Interest")
    sort_order: int | None = Field(default=None, alias="sortOrder", description="Sort order of the interest")
    created_when: datetime | None = Field(default=None, alias="createdWhen", description="Created when")
    last_amended_when: datetime | None = Field(default=None, alias="lastAmendedWhen", description="Last amended when")
    deleted_when: datetime | None = Field(default=None, alias="deletedWhen", description="Deleted when")
    is_correction: bool = Field(default=False, alias="isCorrection", description="Is correction")
    child_interests: list["RegisteredInterest"] | None = Field(default=None, alias="childInterests", description="Child interests")

class Staff(BaseAPIModel):
    """Staff model from Members API."""
    surname: str | None = Field(default=None, description="Surname of the staff")
    forename: str | None = Field(default=None, description="Forename of the staff")
    title: str | None = Field(default=None, description="Title of the staff")
    details: str | None = Field(default=None, description="Details of the staff")
    

class RegisteredInterestCategory(BaseAPIModel):
    """Interest category model from Members API."""
    id: int = Field(default=0, description="ID of the interest category")
    name: str | None = Field(default=None, description="Name of the interest category")
    sort_order: int | None = Field(default=None, alias="sortOrder", description="Sort order of the interest category")
    interests: list[RegisteredInterest] | None = Field(default=None, description="Interests")
    

class MembersInterests(BaseAPIModel):
    """Members interests model from Members API."""
    member: Member | None = Field(default=None, description="Member")
    interest_categories: list[RegisteredInterestCategory] | None = Field(default=None, alias="interestCategories", description="Interest categories")

class MembersStaff(BaseAPIModel):
    """Members staff model from Members API."""
    member: Member | None = Field(default=None, description="Member")
    staff: list[Staff] | None = Field(default=None, description="Staff")   

G = TypeVar("G", bound=BaseAPIModel)


class Item(BaseAPIModel, Generic[G]):
    value: G | None = Field(default=None, description="Resource")
    links: list[Link] | None = Field(
        default=None, description="Links to related resources"
    )


class MemberItem(Item[Member]):
    """Wrapper for member data."""


class DebateContributionItem(Item[DebateContribution]):
    """Wrapper for debate contribution data."""


class MembersInterestsItem(Item[MembersInterests]):
    """Wrapper for member interests data."""

class MembersStaffItem(Item[MembersStaff]):
    """Wrapper for member staff data."""

T = TypeVar("T", bound=BaseAPIModel)


class MembersServiceSearchResult(BaseAPIModel, Generic[T]):
    """Search result for members from Members API."""

    items: list[T] | None = Field(default=None, description="List of members")
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
    result_type: str | None = Field(
        default=None, alias="resultType", description="How the results were matched"
    )


class MemberMembersServiceSearchResult(MembersServiceSearchResult[MemberItem]):
    """Search result for members from Members API."""


class DebateContributionMembersServiceSearchResult(
    MembersServiceSearchResult[DebateContributionItem]
):
    """Search result for debate contributions from Members API."""


class MembersInterestsMembersServiceSearchResult(MembersServiceSearchResult[MembersInterestsItem]):
    """Search result for members interests from Members API."""


class MembersStaffMembersServiceSearchResult(MembersServiceSearchResult[MembersStaffItem]):
    """Search result for members staff from Members API."""


class LordsInterestsRegisterParams(BaseAPIModel):
    search_term: str | None = Field(default=None, alias="searchTerm", description="Registered interests containing search term")
    page: int | None = Field(default=None, description="Page of results to return, default 0. Results per page 20")
    include_deleted: bool = Field(default=False, alias="includeDeleted", description="Registered interests that have been deleted")


class LordsInterestsStaffParams(BaseAPIModel):
    search_term: str | None = Field(default=None, alias="searchTerm", description="Staff containing search term")
    page: int | None = Field(default=None, description="Page of results to return, default 0. Results per page 20")
    

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
