"""Sensor platform for Otodata Tank Monitor."""

from datetime import datetime, timezone

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Otodata Tank sensors from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            OtodataTankLevelSensor(coordinator, entry),
            OtodataLastReadSensor(coordinator, entry),
        ]
    )


class OtodataTankLevelSensor(CoordinatorEntity, SensorEntity):
    """Sensor for the propane tank level percentage."""

    _attr_has_entity_name = True
    _attr_name = "Tank Level"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:propane-tank"

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        serial = str(coordinator.data["serialNumber"])
        self._attr_unique_id = f"{serial}_tank_level"
        self._attr_device_info = _device_info(coordinator.data, entry)

    @property
    def native_value(self) -> int | None:
        """Return the tank level percentage."""
        if self.coordinator.data:
            return self.coordinator.data.get("lastLevel")
        return None


class OtodataLastReadSensor(CoordinatorEntity, SensorEntity):
    """Sensor for the last read timestamp."""

    _attr_has_entity_name = True
    _attr_name = "Last Read"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_icon = "mdi:clock-outline"

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        serial = str(coordinator.data["serialNumber"])
        self._attr_unique_id = f"{serial}_last_read"
        self._attr_device_info = _device_info(coordinator.data, entry)

    @property
    def native_value(self) -> datetime | None:
        """Return the last read timestamp."""
        if self.coordinator.data:
            last_read = self.coordinator.data.get("lastRead")
            if last_read:
                return datetime.fromisoformat(last_read).replace(tzinfo=timezone.utc)
        return None


def _device_info(data: dict, entry: ConfigEntry) -> dict:
    """Return device info for grouping entities."""
    serial = str(data["serialNumber"])
    return {
        "identifiers": {(DOMAIN, serial)},
        "name": f"Propane Tank ({serial})",
        "manufacturer": "Otodata",
        "model": data.get("model", "Unknown"),
        "serial_number": serial,
        "entry_type": None,
    }
