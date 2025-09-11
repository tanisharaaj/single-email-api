from pydantic import BaseModel, EmailStr
from typing import Optional


class MemberRequest(BaseModel):
    member_id: str
    email: EmailStr
    brand_name: str
    app_name: str
    appstore_link: str
    playstore_link: str
    website_portal: str
    cta_url: Optional[str] = None


class NotifyRequest(BaseModel):
    member: MemberRequest  # only one member at a time


class NotifyResponse(BaseModel):
    status: str
    run_id: str | None = None
    message: str
