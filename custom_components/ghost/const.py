"""Constants for the Ghost integration."""

DOMAIN: str = "ghost"

CONF_ADMIN_API_KEY: str = "admin_api_key"
CONF_API_URL: str = "api_url"

DEFAULT_SCAN_INTERVAL: int = 300  # 5 minutes

# Device info
MANUFACTURER: str = "Ghost Foundation"
MODEL: str = "Ghost"
DEFAULT_TITLE: str = "Ghost"
CURRENCY: str = "USD"

# Webhook events to subscribe to
# Note: member.edited excluded - too high volume (fires on every email open/click)
WEBHOOK_EVENTS: list[str] = [
    "member.added",
    "member.deleted",
    "post.published",
]
