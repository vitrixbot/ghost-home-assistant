"""DataUpdateCoordinator for Ghost."""

import asyncio
from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import GhostAdminAPI
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class GhostDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Ghost data."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: GhostAdminAPI,
        site_title: str,
    ) -> None:
        """Initialize the coordinator."""
        self.api = api
        self.site_title = site_title

        super().__init__(
            hass,
            _LOGGER,
            name=f"Ghost ({site_title})",
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> dict:
        """Fetch data from Ghost API."""
        try:
            # Parallelize all API calls for faster updates
            (
                site,
                posts,
                members,
                latest_post,
                latest_email,
                activitypub,
                mrr,
                comments,
                newsletters,
            ) = await asyncio.gather(
                self.api.get_site(),
                self.api.get_posts_count(),
                self.api.get_members_count(),
                self.api.get_latest_post(),
                self.api.get_latest_email(),
                self.api.get_activitypub_stats(),
                self.api.get_mrr(),
                self.api.get_comments_count(),
                self.api.get_newsletters(),
            )

            return {
                "site": site,
                "posts": posts,
                "members": members,
                "latest_post": latest_post,
                "latest_email": latest_email,
                "activitypub": activitypub,
                "mrr": mrr,
                "comments": comments,
                "newsletters": newsletters,
            }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with Ghost API: {err}") from err
