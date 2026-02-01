"""Config flow for Ghost integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_URL
from homeassistant.helpers.network import get_url, NoURLAvailableError

from .api import GhostAdminAPI
from .const import CONF_ADMIN_API_KEY, CONF_ENABLE_WEBHOOKS, CONF_WEBHOOK_URL, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_URL): str,
        vol.Required(CONF_ADMIN_API_KEY): str,
    }
)


class GhostConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Ghost."""

    VERSION = 1
    
    def __init__(self) -> None:
        """Initialize the config flow."""
        self._site_url: str | None = None
        self._admin_api_key: str | None = None
        self._site_title: str | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        
        if user_input is not None:
            site_url = user_input[CONF_URL].rstrip("/")
            admin_api_key = user_input[CONF_ADMIN_API_KEY]
            
            # Validate the API key format
            if ":" not in admin_api_key:
                errors["base"] = "invalid_api_key"
            else:
                # Test the connection
                api = GhostAdminAPI(site_url, admin_api_key)
                try:
                    site = await api.get_site()
                    self._site_title = site.get("title", "Ghost")
                    self._site_url = site_url
                    self._admin_api_key = admin_api_key
                    
                    # Check if already configured
                    await self.async_set_unique_id(site_url)
                    self._abort_if_unique_id_configured()
                    
                    # Move to webhook configuration step
                    return await self.async_step_webhooks()
                    
                except Exception as err:
                    _LOGGER.error("Failed to connect to Ghost: %s", err)
                    errors["base"] = "cannot_connect"
                finally:
                    await api.close()

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
            description_placeholders={
                "docs_url": "https://account.ghost.org/?r=settings/integrations",
            },
        )

    async def async_step_webhooks(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle webhook configuration step."""
        errors: dict[str, str] = {}
        
        # Try to detect HA external URL
        default_webhook_url = ""
        try:
            default_webhook_url = get_url(self.hass, allow_internal=False)
        except NoURLAvailableError:
            pass
        
        if user_input is not None:
            enable_webhooks = user_input.get(CONF_ENABLE_WEBHOOKS, False)
            webhook_url = user_input.get(CONF_WEBHOOK_URL, "").rstrip("/")
            
            # Validate webhook URL if webhooks are enabled
            if enable_webhooks and not webhook_url:
                errors["base"] = "webhook_url_required"
            elif enable_webhooks and not webhook_url.startswith("https://"):
                errors["base"] = "webhook_url_https"
            else:
                return self.async_create_entry(
                    title=self._site_title,
                    data={
                        CONF_URL: self._site_url,
                        CONF_ADMIN_API_KEY: self._admin_api_key,
                        CONF_ENABLE_WEBHOOKS: enable_webhooks,
                        CONF_WEBHOOK_URL: webhook_url if enable_webhooks else "",
                    },
                )
        
        webhook_schema = vol.Schema(
            {
                vol.Optional(CONF_ENABLE_WEBHOOKS, default=False): bool,
                vol.Optional(CONF_WEBHOOK_URL, default=default_webhook_url): str,
            }
        )
        
        return self.async_show_form(
            step_id="webhooks",
            data_schema=webhook_schema,
            errors=errors,
            description_placeholders={
                "site_title": self._site_title,
            },
        )
