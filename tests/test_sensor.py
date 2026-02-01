"""Tests for Ghost sensors."""

from unittest.mock import AsyncMock, patch

import pytest

from homeassistant.core import HomeAssistant

from custom_components.ghost.const import DOMAIN

from .conftest import API_URL


async def test_sensors_created(
    hass: HomeAssistant, mock_ghost_api: AsyncMock, mock_config_entry, mock_ghost_data
) -> None:
    """Test that sensors are created."""
    mock_config_entry.add_to_hass(hass)

    with (
        patch("custom_components.ghost.GhostAdminAPI", return_value=mock_ghost_api),
        patch("custom_components.ghost.coordinator.GhostAdminAPI", return_value=mock_ghost_api),
    ):
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

    # Check core sensors exist
    assert hass.states.get("sensor.test_ghost_total_members") is not None
    assert hass.states.get("sensor.test_ghost_paid_members") is not None
    assert hass.states.get("sensor.test_ghost_free_members") is not None
    assert hass.states.get("sensor.test_ghost_mrr") is not None
    assert hass.states.get("sensor.test_ghost_arr") is not None
    assert hass.states.get("sensor.test_ghost_published_posts") is not None
    assert hass.states.get("sensor.test_ghost_latest_post") is not None


async def test_member_sensors_values(
    hass: HomeAssistant, mock_ghost_api: AsyncMock, mock_config_entry, mock_ghost_data
) -> None:
    """Test member sensor values."""
    mock_config_entry.add_to_hass(hass)

    with (
        patch("custom_components.ghost.GhostAdminAPI", return_value=mock_ghost_api),
        patch("custom_components.ghost.coordinator.GhostAdminAPI", return_value=mock_ghost_api),
    ):
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

    total = hass.states.get("sensor.test_ghost_total_members")
    assert total.state == "1000"

    paid = hass.states.get("sensor.test_ghost_paid_members")
    assert paid.state == "100"

    free = hass.states.get("sensor.test_ghost_free_members")
    assert free.state == "850"

    comped = hass.states.get("sensor.test_ghost_comped_members")
    assert comped.state == "50"


async def test_revenue_sensors_values(
    hass: HomeAssistant, mock_ghost_api: AsyncMock, mock_config_entry, mock_ghost_data
) -> None:
    """Test revenue sensor values."""
    mock_config_entry.add_to_hass(hass)

    with (
        patch("custom_components.ghost.GhostAdminAPI", return_value=mock_ghost_api),
        patch("custom_components.ghost.coordinator.GhostAdminAPI", return_value=mock_ghost_api),
    ):
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

    # MRR: 500000 cents = $5000
    mrr = hass.states.get("sensor.test_ghost_mrr")
    assert mrr.state == "5000"

    # ARR: $5000 * 12 = $60000
    arr = hass.states.get("sensor.test_ghost_arr")
    assert arr.state == "60000"


async def test_post_sensors_values(
    hass: HomeAssistant, mock_ghost_api: AsyncMock, mock_config_entry, mock_ghost_data
) -> None:
    """Test post sensor values."""
    mock_config_entry.add_to_hass(hass)

    with (
        patch("custom_components.ghost.GhostAdminAPI", return_value=mock_ghost_api),
        patch("custom_components.ghost.coordinator.GhostAdminAPI", return_value=mock_ghost_api),
    ):
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

    published = hass.states.get("sensor.test_ghost_published_posts")
    assert published.state == "42"

    drafts = hass.states.get("sensor.test_ghost_draft_posts")
    assert drafts.state == "5"

    scheduled = hass.states.get("sensor.test_ghost_scheduled_posts")
    assert scheduled.state == "2"


async def test_latest_post_sensor(
    hass: HomeAssistant, mock_ghost_api: AsyncMock, mock_config_entry, mock_ghost_data
) -> None:
    """Test latest post sensor and attributes."""
    mock_config_entry.add_to_hass(hass)

    with (
        patch("custom_components.ghost.GhostAdminAPI", return_value=mock_ghost_api),
        patch("custom_components.ghost.coordinator.GhostAdminAPI", return_value=mock_ghost_api),
    ):
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

    latest = hass.states.get("sensor.test_ghost_latest_post")
    assert latest.state == "Latest Post"
    assert latest.attributes["url"] == f"{API_URL}/latest-post/"
    assert latest.attributes["slug"] == "latest-post"


async def test_email_sensors_values(
    hass: HomeAssistant, mock_ghost_api: AsyncMock, mock_config_entry, mock_ghost_data
) -> None:
    """Test email sensor values."""
    mock_config_entry.add_to_hass(hass)

    with (
        patch("custom_components.ghost.GhostAdminAPI", return_value=mock_ghost_api),
        patch("custom_components.ghost.coordinator.GhostAdminAPI", return_value=mock_ghost_api),
    ):
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

    latest_email = hass.states.get("sensor.test_ghost_latest_email")
    assert latest_email.state == "Newsletter #1"

    open_rate = hass.states.get("sensor.test_ghost_latest_email_open_rate")
    assert open_rate.state == "40"

    click_rate = hass.states.get("sensor.test_ghost_latest_email_click_rate")
    assert click_rate.state == "10"


async def test_activitypub_sensors_values(
    hass: HomeAssistant, mock_ghost_api: AsyncMock, mock_config_entry, mock_ghost_data
) -> None:
    """Test ActivityPub sensor values."""
    mock_config_entry.add_to_hass(hass)

    with (
        patch("custom_components.ghost.GhostAdminAPI", return_value=mock_ghost_api),
        patch("custom_components.ghost.coordinator.GhostAdminAPI", return_value=mock_ghost_api),
    ):
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

    followers = hass.states.get("sensor.test_ghost_socialweb_followers")
    assert followers.state == "150"

    following = hass.states.get("sensor.test_ghost_socialweb_following")
    assert following.state == "25"


async def test_newsletter_sensors_created(
    hass: HomeAssistant, mock_ghost_api: AsyncMock, mock_config_entry, mock_ghost_data
) -> None:
    """Test that newsletter sensors are created for active newsletters only."""
    mock_config_entry.add_to_hass(hass)

    with (
        patch("custom_components.ghost.GhostAdminAPI", return_value=mock_ghost_api),
        patch("custom_components.ghost.coordinator.GhostAdminAPI", return_value=mock_ghost_api),
    ):
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

    # Active newsletter should have a sensor
    weekly = hass.states.get("sensor.test_ghost_weekly_subscribers")
    assert weekly is not None
    assert weekly.state == "800"

    # Archived newsletter should not have a sensor
    archive = hass.states.get("sensor.test_ghost_archive_subscribers")
    assert archive is None


async def test_device_info(
    hass: HomeAssistant, mock_ghost_api: AsyncMock, mock_config_entry, mock_ghost_data
) -> None:
    """Test device info is set correctly."""
    from homeassistant.helpers import device_registry as dr, entity_registry as er

    mock_config_entry.add_to_hass(hass)

    with (
        patch("custom_components.ghost.GhostAdminAPI", return_value=mock_ghost_api),
        patch("custom_components.ghost.coordinator.GhostAdminAPI", return_value=mock_ghost_api),
    ):
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("sensor.test_ghost_total_members")
    assert entry is not None

    device_registry = dr.async_get(hass)
    device = device_registry.async_get(entry.device_id)
    assert device is not None
    assert device.manufacturer == "Ghost Foundation"
    assert device.model == "Ghost"
