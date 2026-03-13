from pydantic import BaseModel, field_validator, model_validator

from app.constants import SEGMENT_OPTIONS, STATUS_OPTIONS


class EnterpriseBase(BaseModel):
    @field_validator(
        "business_name",
        "owner_name",
        "city",
        "contact",
        "description",
        mode="before",
        check_fields=False,
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

    @field_validator("segment", check_fields=False)
    @classmethod
    def validate_segment(cls, value: str | None) -> str | None:
        if value is None:
            return None

        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("Segment cannot be empty")
        if cleaned_value not in SEGMENT_OPTIONS:
            raise ValueError("Invalid segment")
        return cleaned_value

    @field_validator("status", check_fields=False)
    @classmethod
    def validate_status(cls, value: str | None) -> str | None:
        if value is None:
            return None

        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("Status cannot be empty")
        if cleaned_value not in STATUS_OPTIONS:
            raise ValueError("Invalid status")
        return cleaned_value


class EnterpriseCreate(EnterpriseBase):
    business_name: str
    owner_name: str
    city: str
    segment: str
    contact: str
    status: str
    description: str | None = None


class EnterpriseUpdate(EnterpriseBase):
    business_name: str | None = None
    owner_name: str | None = None
    city: str | None = None
    segment: str | None = None
    contact: str | None = None
    status: str | None = None
    description: str | None = None

    @model_validator(mode="after")
    def validate_at_least_one_field(self) -> "EnterpriseUpdate":
        if not self.model_dump(exclude_none=True):
            raise ValueError("At least one field must be provided")
        return self
