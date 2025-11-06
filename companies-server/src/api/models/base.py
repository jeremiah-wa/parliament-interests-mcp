from pydantic import BaseModel, ConfigDict, field_validator


class BaseAPIModel(BaseModel):
    """Base model for API data."""

    model_config = ConfigDict(
        extra="ignore",
        validate_by_name=True,
        validate_by_alias=True
    )

    @field_validator("*", mode="before")
    def str_none_to_none(cls, value):
        """Convert string 'None' to actual None."""
        return None if value == "None" else value

