"""iRacing data reader for RaceBuff

Provides structured data access and conversion for iRacing telemetry
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class IRacingReader:
    """Process iRacing telemetry data"""

    # iRacing telemetry variable mapping
    MAPPING = {
        # Speed and motion
        "speed": "Speed",  # m/s
        "throttle": "Throttle",  # 0-1
        "brake": "Brake",  # 0-1
        "clutch": "Clutch",  # 0-1
        "gear": "Gear",  # -1=R, 0=N, 1+=gears
        "rpm": "RPM",
        "max_rpm": "EngineMaxRPM",
        # Brake
        "brake_bias": "BrakeBias",  # 0-100 or 0-1
        "brake_pressure_fl": "BrakePressure_0",
        "brake_pressure_fr": "BrakePressure_1",
        "brake_pressure_rl": "BrakePressure_2",
        "brake_pressure_rr": "BrakePressure_3",
        "brake_temp_fl": "BrakeTemp_0",
        "brake_temp_fr": "BrakeTemp_1",
        "brake_temp_rl": "BrakeTemp_2",
        "brake_temp_rr": "BrakeTemp_3",
        # Steering and suspension
        "steering_angle": "SteeringWheelAngle",  # radians
        "steering_wheel_torque": "SteeringWheelTorque",  # Nm
        "suspension_travel_fl": "SuspensionTravel_0",  # front left
        "suspension_travel_fr": "SuspensionTravel_1",
        "suspension_travel_rl": "SuspensionTravel_2",
        "suspension_travel_rr": "SuspensionTravel_3",
        # Wheel slip
        "slip_angle_fl": "LFasterSlipAngle",
        "slip_angle_fr": "RFasterSlipAngle",
        "slip_angle_rl": "LRasterSlipAngle",
        "slip_angle_rr": "RRasterSlipAngle",
        # Tires
        "tire_temp_fl": "TireTemp_0",  # celsius
        "tire_temp_fr": "TireTemp_1",
        "tire_temp_rl": "TireTemp_2",
        "tire_temp_rr": "TireTemp_3",
        "tire_wear_fl": "TireWear_0",  # 0-1
        "tire_wear_fr": "TireWear_1",
        "tire_wear_rl": "TireWear_2",
        "tire_wear_rr": "TireWear_3",
        # Fuel
        "fuel_level": "FuelLevel",  # liters
        "fuel_pressure": "FuelPressure",  # bar
        "fuel_capacity": "FuelCapacity",  # liters, may be in session
        # Engine
        "engine_temp": "WaterTemp",  # celsius
        "oil_temp": "OilTemp",
        "oil_pressure": "OilPressure",  # bar
        # G-forces
        "accel_x": "LongAccel",
        "accel_y": "LatAccel",
        "accel_z": "VertAccel",
        # Lap info
        "lap": "Lap",
        "lap_dist_pct": "LapDistPct",  # 0-1
        "lap_dist": "LapDist",  # meters into current lap
        "current_lap_time": "LapCurrentLapTime",  # seconds
        "last_lap_time": "LastLapTime",
        "best_lap_time": "BestLapTime",
        # Session info
        "session_time": "SessionTime",  # seconds
        "session_state": "SessionState",
        "session_type": "SessionType",
        "session_num": "SessionNum",
        "session_flags": "SessionFlags",  # bitmask
        "session_time_total": "SessionTimeTotal",
        "session_time_remain": "SessionTimeRemain",
        "session_laps_total": "SessionLapsTotal",
        "session_laps_remain": "SessionLapsRemain",
        "track_air_temp": "TrackAirTemp",  # WeekendInfo/session, celsius
        "track_surface_temp": "TrackSurfaceTemp",
        "track_length": "TrackLength",  # meters, may be in session
        # Driver info
        "is_on_track": "IsOnTrack",
        "is_paused": "IsPaused",
        # Switch
        "headlights": "Headlights",  # 0/1
        "ignition": "Ignition",  # 0/1
        "wiper": "Wiper",  # 0/1
        "speed_limiter": "SpeedLimiter",  # 0/1
    }

    def __init__(self, connector) -> None:
        """Initialize iRacing reader
        
        Args:
            connector: IRacingConnector instance
        """
        self.connector = connector
        self._last_data = {}

    def read(self) -> Dict[str, Any]:
        """Read and process current iRacing data
        
        Returns:
            Dictionary with processed telemetry data
        """
        data = {}
        
        if not self.connector.is_connected:
            return data
        
        try:
            # Read mapped variables
            for key, var_name in self.MAPPING.items():
                value = self.connector.get_var(var_name)
                if value is not None:
                    data[key] = value
            
            # Additional computed values
            data["connected"] = True
            data["active"] = self.connector.is_active
            data["timestamp"] = self.connector.last_update
            
            self._last_data = data
            return data
            
        except Exception as e:
            logger.error(f"iRacing: read error: {e}")
            return {"connected": False}

    def get(self, key: str, default: Any = None) -> Any:
        """Get value from last read data or live from connector"""
        var_name = self.MAPPING.get(key, key)
        val = self.connector.get_var(var_name)
        if val is not None:
            return val
        return self._last_data.get(key, default)

    def get_float(self, key: str, default: float = 0.0) -> float:
        """Get float value from connector (live data)"""
        var_name = self.MAPPING.get(key, key)
        return self.connector.get_float(var_name, default)

    def get_int(self, key: str, default: int = 0) -> int:
        """Get integer value from connector (live data)"""
        var_name = self.MAPPING.get(key, key)
        return self.connector.get_int(var_name, default)

    def get_int_at(self, var_name: str, index: int, default: int = 0) -> int:
        """Get integer at index from array variable (e.g. CarIdxPosition)."""
        try:
            val = self.connector.get_var_at(var_name, index, default)
            return int(val) if val is not None else default
        except (ValueError, TypeError):
            return default

    def get_float_at(self, var_name: str, index: int, default: float = 0.0) -> float:
        """Get float at index from array variable (e.g. CarIdxLapDistPct, CarIdxBestLapTime)."""
        try:
            val = self.connector.get_var_at(var_name, index, default)
            return float(val) if val is not None else default
        except (ValueError, TypeError):
            return default
