"""Constants for the Ghost integration."""

DOMAIN = "ghost"

CONF_ADMIN_API_KEY = "admin_api_key"
CONF_API_URL = "api_url"

DEFAULT_SCAN_INTERVAL = 300  # 5 minutes

# Webhook events to subscribe to
WEBHOOK_EVENTS = [
    "member.added",
    "member.edited",
    "member.deleted",
    "post.published",
]
