# Ghost Integration for Home Assistant

A Home Assistant integration for [Ghost](https://ghost.org), the open source publishing platform.

## Features

This integration creates sensors for your Ghost site:

- **Total Members** - Total number of newsletter subscribers
- **Paid Members** - Number of paying subscribers
- **Free Members** - Number of free subscribers
- **Published Posts** - Number of published posts
- **Draft Posts** - Number of draft posts
- **Scheduled Posts** - Number of scheduled posts
- **Latest Post** - Title of the most recently published post (with URL in attributes)

## Installation

### Manual Installation

1. Copy the `custom_components/ghost` folder to your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant
3. Go to Settings → Devices & Services → Add Integration → Ghost
4. Enter your Ghost site URL and Admin API key

### Getting Your Admin API Key

1. Log in to your Ghost Admin panel
2. Go to Settings → Integrations
3. Click "Add custom integration"
4. Name it "Home Assistant" (or whatever you prefer)
5. Copy the Admin API Key (it looks like `abc123:def456789...`)

## Configuration

The integration is configured via the UI. You'll need:

- **Site URL**: Your Ghost site URL (e.g., `https://yoursite.com`)
- **Admin API Key**: Your Ghost Admin API key

## Sensors

All sensors update every 5 minutes by default.

| Sensor | Description |
|--------|-------------|
| `sensor.ghost_total_members` | Total subscriber count |
| `sensor.ghost_paid_members` | Paid subscriber count |
| `sensor.ghost_free_members` | Free subscriber count |
| `sensor.ghost_published_posts` | Published post count |
| `sensor.ghost_draft_posts` | Draft post count |
| `sensor.ghost_scheduled_posts` | Scheduled post count |
| `sensor.ghost_latest_post` | Title of latest post |

## Example Automations

### Notify on new member milestone

```yaml
automation:
  - alias: "Ghost Member Milestone"
    trigger:
      - platform: numeric_state
        entity_id: sensor.ghost_total_members
        above: 1000
    action:
      - service: notify.mobile_app
        data:
          message: "🎉 Ghost just hit {{ states('sensor.ghost_total_members') }} members!"
```

### Announce new post

```yaml
automation:
  - alias: "New Ghost Post Published"
    trigger:
      - platform: state
        entity_id: sensor.ghost_latest_post
    action:
      - service: tts.speak
        data:
          message: "New post published: {{ states('sensor.ghost_latest_post') }}"
```

## Development

This integration is designed to eventually be submitted to the Home Assistant core integrations. It follows Home Assistant's development guidelines and best practices.

## License

MIT License - see [LICENSE](LICENSE) for details.
