from pydantic import BaseModel, field_validator

from app.constants import SEGMENT_OPTIONS, STATUS_OPTIONS


class EnterpriseCreate(BaseModel):
    business_name: str
    owner_name: str
    city: str
    segment: str
    contact: str
    status: str
    description: str | None = None

    @field_validator(
        "business_name",
        "owner_name",
        "city",
        "contact",
        "description",
        mode="before",
    )
    @classmethod
    def validate_text_fields(cls, value: str | None) -> str | None:
        if value is None:
            return None

        if not isinstance(value, str):
            raise ValueError("Field must be a string")

        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("Field cannot be empty")

        return cleaned_value

    @field_validator("segment")
    @classmethod
    def validate_segment(cls, value: str) -> str:
        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("Segment cannot be empty")
        if cleaned_value not in SEGMENT_OPTIONS:
            raise ValueError("Invalid segment")
        return cleaned_value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("Status cannot be empty")
        if cleaned_value not in STATUS_OPTIONS:
            raise ValueError("Invalid status")
        return cleaned_value
