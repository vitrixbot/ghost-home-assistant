"""Tests for Ghost data coordinator."""

from unittest.mock import AsyncMock, patch

import pytest

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.ghost.coordinator import GhostDataUpdateCoordinator

from .conftest import API_URL


async def test_coordinator_update(
    hass: HomeAssistant, mock_ghost_api: AsyncMock, mock_ghost_data
) -> None:
    """Test coordinator fetches data successfully."""
    coordinator = GhostDataUpdateCoordinator(hass, mock_ghost_api, "Test Ghost")

    await coordinator.async_refresh()

    assert coordinator.data is not None
    assert coordinator.data["site"]["title"] == "Test Ghost"
    assert coordinator.data["members"]["total"] == 1000
    assert coordinator.data["posts"]["published"] == 42


async def test_coordinator_parallel_requests(
    hass: HomeAssistant, mock_ghost_api: AsyncMock
) -> None:
    """Test coordinator makes parallel API requests."""
    coordinator = GhostDataUpdateCoordinator(hass, mock_ghost_api, "Test Ghost")

    await coordinator.async_refresh()

    # Verify all API methods were called
    mock_ghost_api.get_site.assert_called_once()
    mock_ghost_api.get_posts_count.assert_called_once()
    mock_ghost_api.get_members_count.assert_called_once()
    mock_ghost_api.get_latest_post.assert_called_once()
    mock_ghost_api.get_latest_email.assert_called_once()
    mock_ghost_api.get_activitypub_stats.assert_called_once()
    mock_ghost_api.get_mrr.assert_called_once()
    mock_ghost_api.get_comments_count.assert_called_once()
    mock_ghost_api.get_newsletters.assert_called_once()


async def test_coordinator_auth_error(hass: HomeAssistant) -> None:
    """Test coordinator raises ConfigEntryAuthFailed on auth error."""
    from aioghost.exceptions import GhostAuthError

    mock_api = AsyncMock()
    mock_api.get_site.side_effect = GhostAuthError("Invalid API key")

    coordinator = GhostDataUpdateCoordinator(hass, mock_api, "Test Ghost")

    with pytest.raises(ConfigEntryAuthFailed):
        await coordinator.async_refresh()


async def test_coordinator_connection_error(hass: HomeAssistant) -> None:
    """Test coordinator raises UpdateFailed on connection error."""
    from aioghost.exceptions import GhostConnectionError

    mock_api = AsyncMock()
    mock_api.get_site.side_effect = GhostConnectionError("Connection failed")

    coordinator = GhostDataUpdateCoordinator(hass, mock_api, "Test Ghost")

    with pytest.raises(UpdateFailed, match="Error communicating with Ghost API"):
        await coordinator.async_refresh()


async def test_coordinator_generic_error(hass: HomeAssistant) -> None:
    """Test coordinator raises UpdateFailed on generic error."""
    from aioghost.exceptions import GhostError

    mock_api = AsyncMock()
    mock_api.get_site.side_effect = GhostError("Something went wrong")

    coordinator = GhostDataUpdateCoordinator(hass, mock_api, "Test Ghost")

    with pytest.raises(UpdateFailed):
        await coordinator.async_refresh()


async def test_coordinator_name(hass: HomeAssistant, mock_ghost_api: AsyncMock) -> None:
    """Test coordinator has correct name."""
    coordinator = GhostDataUpdateCoordinator(hass, mock_ghost_api, "My Site")

    assert coordinator.name == "Ghost (My Site)"


async def test_coordinator_update_interval(
    hass: HomeAssistant, mock_ghost_api: AsyncMock
) -> None:
    """Test coordinator has correct update interval."""
    from datetime import timedelta

    from custom_components.ghost.const import DEFAULT_SCAN_INTERVAL

    coordinator = GhostDataUpdateCoordinator(hass, mock_ghost_api, "Test Ghost")

    assert coordinator.update_interval == timedelta(seconds=DEFAULT_SCAN_INTERVAL)
