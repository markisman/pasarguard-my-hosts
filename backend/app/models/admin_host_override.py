from pydantic import BaseModel, ConfigDict, Field


class AdminHostOverrideItem(BaseModel):
    host_id: int
    display_name: str | None = None
    sort_order: int | None = None
    is_disabled: bool = False


class AdminHostOverrideBulk(BaseModel):
    items: list[AdminHostOverrideItem] = Field(default_factory=list)


class AdminHostOverrideResponse(AdminHostOverrideItem):
    model_config = ConfigDict(from_attributes=True)


class MyHostResponse(BaseModel):
    """A host as seen by the current admin, with their override applied."""

    host_id: int
    inbound_tag: str | None = None
    address: list[str] = Field(default_factory=list)
    port: int | None = None
    # Default (global) values
    remark: str
    priority: int
    is_disabled: bool = False
    # This admin's override (None if not set)
    display_name: str | None = None
    sort_order: int | None = None
    override_disabled: bool = False


class MyHostsResponse(BaseModel):
    hosts: list[MyHostResponse] = Field(default_factory=list)
