from temporalio import activity
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.settings import settings
from anyio import to_thread

REQUIRED_KEYS = {
    "email", "brand_name", "app_name",
    "appstore_link", "playstore_link", "website_portal",
}

@activity.defn(name="send_email_activity")  # decorated
async def send_email_activity(member: dict) -> dict:
    print(f"Sending email to {member['email']}")

    missing = [k for k in REQUIRED_KEYS if not member.get(k)]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")

    message = Mail(
        from_email=settings.SENDGRID_FROM_EMAIL,
        to_emails=member["email"],
    )
    message.template_id = settings.SENDGRID_TEMPLATE_ID
    dyn = {k: member[k] for k in REQUIRED_KEYS if member.get(k)}
    if member.get("cta_url"):
        dyn["cta_url"] = member["cta_url"]
    message.dynamic_template_data = dyn

    sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    resp = await to_thread.run_sync(lambda: sg.send(message))

    print(f"SendGrid responded with {resp.status_code}")
    return {"status_code": resp.status_code,
            "message": "sent" if 200 <= resp.status_code < 300 else "failed"}
