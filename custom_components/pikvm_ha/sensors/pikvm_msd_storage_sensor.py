"""PiKVM MSD Storage Sensor."""
from ..sensor import PiKVMBaseSensor

class PiKVMSDStorageSensor(PiKVMBaseSensor):
    """Representation of a PiKVM MSD storage sensor."""

    def __init__(self, coordinator, device_info, unique_id_base):
        """Initialize the sensor."""
        super().__init__(coordinator, device_info, unique_id_base, "msd_storage", "PiKVM MSD Storage", "%", "mdi:database")

    @property
    def state(self):
        """Return the state of the sensor."""
        total_size = self.coordinator.data["msd"]["storage"]["size"]
        free_size = self.coordinator.data["msd"]["storage"]["free"]
        if total_size > 0:
            return round((free_size / total_size) * 100, 2)
        return 0

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attributes = super().extra_state_attributes
        storage_data = self.coordinator.data["msd"]["storage"]
        if storage_data:
            attributes["total_size_mb"] = round(storage_data["size"] / (1024 * 1024), 2)
            attributes["free_size_mb"] = round(storage_data["free"] / (1024 * 1024), 2)
            attributes["used_size_mb"] = round((storage_data["size"] - storage_data["free"]) / (1024 * 1024), 2)
            attributes["percent_free"] = self.state
        return attributes