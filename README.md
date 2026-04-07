# Otodata Tank Monitor

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=dannyrobinson&repository=OtodataTankMonitor&category=integration)

A Home Assistant custom integration for monitoring propane (or other) tank levels via the [Otodata Nee-Vo](https://neevo.otodata.ca/) platform.

## Features

- **Tank Level** sensor showing the current fill percentage
- **Last Read** sensor showing when the tank was last read (UTC)
- Configurable polling interval (default: 5 minutes)
- Automatic device grouping with serial number and model info
- No API key or authentication required -- uses the public Nee-Vo nameplate URL

## Finding Your Device Code

Your device code is the short string at the end of your Nee-Vo nameplate URL.

For example, if your URL is:

```
https://nv.otodata.com/d/WRvsWk
```

Then your device code is `WRvsWk`.

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click the three dots in the top right corner and select **Custom repositories**
3. Add this repository URL: `https://github.com/dannyrobinson/OtodataTankMonitor`
4. Select **Integration** as the category
5. Click **Add**
6. Search for "Otodata Tank Monitor" in HACS and click **Download**
7. Restart Home Assistant

### Manual Installation

1. Download the `custom_components/otodata_tank` folder from this repository
2. Copy it to your Home Assistant `config/custom_components/` directory
3. Restart Home Assistant

## Configuration

1. Go to **Settings > Devices & Services**
2. Click **+ Add Integration**
3. Search for **Otodata Tank Monitor**
4. Enter your **Device Code** (e.g. `WRvsWk`)
5. Optionally adjust the **Update Interval** (default: 300 seconds)
6. Click **Submit**

## Sensors

| Sensor | Description | Unit |
|--------|-------------|------|
| Tank Level | Current fill percentage | `%` |
| Last Read | Timestamp of the last sensor reading | UTC datetime |

## Example Automations

### Low tank level alert

```yaml
automation:
  - alias: "Propane Tank Low"
    trigger:
      - platform: numeric_state
        entity_id: sensor.propane_tank_SERIAL_tank_level
        below: 25
    action:
      - service: notify.mobile_app
        data:
          title: "Propane Tank Low"
          message: "Your propane tank is at {{ states('sensor.propane_tank_SERIAL_tank_level') }}%"
```

## License

MIT
