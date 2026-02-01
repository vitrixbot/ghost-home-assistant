"""Constants for the Ghost integration."""

DOMAIN: str = "ghost"

CONF_ADMIN_API_KEY: str = "admin_api_key"
CONF_API_URL: str = "api_url"

DEFAULT_SCAN_INTERVAL: int = 300  # 5 minutes

# Webhook events to subscribe to
WEBHOOK_EVENTS: list[str] = [
    "member.added",
    "member.edited",
    "member.deleted",
    "post.published",
]
