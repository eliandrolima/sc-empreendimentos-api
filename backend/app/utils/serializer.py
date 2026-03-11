def serialize_enterprise(enterprise: dict | None) -> dict | None:
    if enterprise is None:
        return None

    serialized_enterprise = dict(enterprise)
    serialized_enterprise["id"] = str(serialized_enterprise.pop("_id"))
    return serialized_enterprise


def serialize_enterprise_list(enterprises: list[dict]) -> list[dict]:
    return [serialize_enterprise(enterprise) for enterprise in enterprises]
