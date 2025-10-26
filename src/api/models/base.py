from pydantic import BaseModel, ConfigDict, Field, field_validator


class BaseAPIModel(BaseModel):
    """Base model for API data."""

    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    @field_validator("*", mode="before")
    def str_none_to_none(cls, value):
        """Convert string 'None' to actual None."""
        return None if value == "None" else value


class BaseParams(BaseModel):
    skip: int = Field(
        default=0, ge=0, description="Number of records to skip", alias="Skip"
    )
    take: int = Field(
        default=20, ge=1, le=20, description="Number of records to return", alias="Take"
    )

    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )


class BaseMember(BaseAPIModel):
    """Member data from Parliament API."""

    id: int = Field(description="ID of the member")
    name_list_as: str | None = Field(
        default=None,
        alias="nameListAs",
        description="Member's current name in the format {surname}, {forename}, for use in an ordered list",
    )
    name_display_as: str | None = Field(
        default=None,
        alias="nameDisplayAs",
        description="Member's current full name, as it should be displayed in text",
    )
    name_full_title: str | None = Field(
        default=None, alias="nameFullTitle", description="Member's full title"
    )
    name_address_as: str | None = Field(
        default=None, alias="nameAddressAs", description="Member's name for addressing"
    )


class Link(BaseAPIModel):
    """HATEOAS Link for retrieving related information."""

    rel: str | None = Field(
        default=None, description="Relationship of the link to the object requested"
    )
    href: str | None = Field(
        default=None,
        description="A complete URL that shows how the action can be performed",
    )
    method: str | None = Field(default=None, description="Request method of the link")
