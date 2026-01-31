#  RaceBuff iRacing API reader adapters
#  Full telemetry mapping: _reader interfaces → iRacing SDK (connector + IRacingReader).

from __future__ import annotations

from ..const_common import STINT_USAGE_DEFAULT
from ..process.weather import WeatherNode
from . import _reader
from . import iracing_connector
from . import iracing_reader


class _Adapter:
    __slots__ = ("connector", "reader")

    def __init__(self, connector: iracing_connector.IRacingConnector, reader: iracing_reader.IRacingReader):
        self.connector = connector
        self.reader = reader


class State(_reader.State, _Adapter):
    def active(self) -> bool:
        return self.connector.is_active

    def paused(self) -> bool:
        return self.connector.is_paused

    def desynced(self, index: int | None = None) -> bool:
        return False

    def version(self) -> str:
        return "iRacing"


class Brake(_reader.Brake, _Adapter):
    def bias_front(self, index: int | None = None) -> float:
        b = self.reader.get_float("brake_bias", 50.0)
        if b > 1.0:  # 0-100 percent
            return b / 100.0
        return max(0.0, min(1.0, b))

    def pressure(self, index: int | None = None, scale: float = 1) -> tuple[float, ...]:
        return (
            self.reader.get_float("brake_pressure_fl", 0.0) * scale,
            self.reader.get_float("brake_pressure_fr", 0.0) * scale,
            self.reader.get_float("brake_pressure_rl", 0.0) * scale,
            self.reader.get_float("brake_pressure_rr", 0.0) * scale,
        )

    def temperature(self, index: int | None = None) -> tuple[float, ...]:
        return (
            self.reader.get_float("brake_temp_fl", 0.0),
            self.reader.get_float("brake_temp_fr", 0.0),
            self.reader.get_float("brake_temp_rl", 0.0),
            self.reader.get_float("brake_temp_rr", 0.0),
        )

    def wear(self, index: int | None = None) -> tuple[float, ...]:
        return (0.0, 0.0, 0.0, 0.0)


class ElectricMotor(_reader.ElectricMotor, _Adapter):
    def state(self, index: int | None = None) -> int:
        return 0

    def battery_charge(self, index: int | None = None) -> float:
        return 0.0

    def rpm(self, index: int | None = None) -> float:
        return 0.0

    def torque(self, index: int | None = None) -> float:
        return 0.0

    def motor_temperature(self, index: int | None = None) -> float:
        return 0.0

    def water_temperature(self, index: int | None = None) -> float:
        return 0.0


class Engine(_reader.Engine, _Adapter):
    def gear(self, index: int | None = None) -> int:
        return self.reader.get_int("gear", 0)

    def gear_max(self, index: int | None = None) -> int:
        return 6

    def rpm(self, index: int | None = None) -> float:
        return self.reader.get_float("rpm", 0.0)

    def rpm_max(self, index: int | None = None) -> float:
        return self.reader.get_float("max_rpm", 8000.0)

    def torque(self, index: int | None = None) -> float:
        return 0.0

    def turbo(self, index: int | None = None) -> float:
        return 0.0

    def oil_temperature(self, index: int | None = None) -> float:
        return self.reader.get_float("oil_temp", 0.0)

    def water_temperature(self, index: int | None = None) -> float:
        return self.reader.get_float("engine_temp", 0.0)


class Inputs(_reader.Inputs, _Adapter):
    def throttle(self, index: int | None = None) -> float:
        return self.reader.get_float("throttle", 0.0)

    def throttle_raw(self, index: int | None = None) -> float:
        return self.reader.get_float("throttle", 0.0)

    def brake(self, index: int | None = None) -> float:
        return self.reader.get_float("brake", 0.0)

    def brake_raw(self, index: int | None = None) -> float:
        return self.reader.get_float("brake", 0.0)

    def clutch(self, index: int | None = None) -> float:
        return self.reader.get_float("clutch", 0.0)

    def clutch_raw(self, index: int | None = None) -> float:
        return self.reader.get_float("clutch", 0.0)

    def steering(self, index: int | None = None) -> float:
        return self._steering_normalized()

    def steering_raw(self, index: int | None = None) -> float:
        """Normalized -1..1 from iRacing SteeringWheelAngle (radians)."""
        return self._steering_normalized()

    def _steering_normalized(self) -> float:
        """Steering -1..1 from iRacing SteeringWheelAngle (radians). Range ±450° = ±half of 900°. Sign inverted so overlay left = wheel left."""
        import math
        angle_rad = self.reader.get_float("steering_angle", 0.0)
        range_deg_half = 450.0  # ±450° for 900° total
        if range_deg_half <= 0:
            return 0.0
        range_rad_half = range_deg_half * math.pi / 180.0
        return max(-1.0, min(1.0, -angle_rad / range_rad_half))

    def steering_shaft_torque(self, index: int | None = None) -> float:
        return self.reader.get_float("steering_wheel_torque", 0.0)

    def steering_range_physical(self, index: int | None = None) -> float:
        return 900.0

    def steering_range_visual(self, index: int | None = None) -> float:
        return 900.0

    def force_feedback(self) -> float:
        return 0.0


class Lap(_reader.Lap, _Adapter):
    def number(self, index: int | None = None) -> int:
        return self.reader.get_int("lap", 0)

    def completed_laps(self, index: int | None = None) -> int:
        return self.reader.get_int("lap", 0)

    def track_length(self) -> float:
        return self.reader.get_float("track_length", 0.0)

    def distance(self, index: int | None = None) -> float:
        idx = 0 if index is None else index
        if idx == 0:
            dist_pct = self.reader.get_float("lap_dist_pct", 0.0)
            length = self.reader.get_float("track_length", 0.0)
            if length > 0:
                return dist_pct * length
            return self.reader.get_float("lap_dist", 0.0)
        length = self.reader.get_float("track_length", 0.0)
        dist_pct = self.reader.get_float_at("CarIdxLapDistPct", idx, 0.0)
        return (dist_pct * length) if length > 0 else 0.0

    def progress(self, index: int | None = None) -> float:
        idx = 0 if index is None else index
        if idx == 0:
            return self.reader.get_float("lap_dist_pct", 0.0)
        return self.reader.get_float_at("CarIdxLapDistPct", idx, 0.0)

    def maximum(self) -> int:
        return max(0, self.reader.get_int("session_laps_total", 0))

    def sector_index(self, index: int | None = None) -> int:
        return 0

    def behind_leader(self, index: int | None = None) -> int:
        idx = 0 if index is None else index
        leader_lap = self.reader.get_int_at("CarIdxLap", 0, 0)
        for i in range(self.reader.connector.get_int("DriverCount", 1)):
            pos = self.reader.get_int_at("CarIdxPosition", i, 0)
            if pos == 1:
                leader_lap = self.reader.get_int_at("CarIdxLap", i, 0)
                break
        car_lap = self.reader.get_int_at("CarIdxLap", idx, 0)
        return max(0, leader_lap - car_lap)

    def behind_next(self, index: int | None = None) -> int:
        idx = 0 if index is None else index
        my_pos = self.reader.get_int_at("CarIdxPosition", idx, 1)
        my_lap = self.reader.get_int_at("CarIdxLap", idx, 0)
        n = self.reader.connector.get_int("DriverCount", 1)
        for i in range(n):
            if self.reader.get_int_at("CarIdxPosition", i, 0) == my_pos + 1:
                return max(0, self.reader.get_int_at("CarIdxLap", i, 0) - my_lap)
        return 0


class Session(_reader.Session, _Adapter):
    def combo_name(self) -> str:
        return "iRacing"

    def track_name(self) -> str:
        name = self.reader.connector.get_var("TrackDisplayName") or self.reader.connector.get_var("TrackName")
        return str(name).strip() if name else "iRacing"

    def identifier(self) -> tuple[int, int, int]:
        return (
            self.reader.get_int("session_num", 0),
            self.reader.connector.get_int("SessionID", 0),
            self.reader.connector.get_int("SubSessionID", 0),
        )

    def elapsed(self) -> float:
        return self.reader.get_float("session_time", 0.0)

    def start(self) -> float:
        return 0.0

    def end(self) -> float:
        total = self.reader.get_float("session_time_total", 0.0)
        return total if total > 0 else 0.0

    def remaining(self) -> float:
        return self.reader.get_float("session_time_remain", 0.0)

    def session_type(self) -> int:
        return self.reader.get_int("session_type", 0)

    def lap_type(self) -> bool:
        return self.reader.get_float("session_time_total", 0.0) <= 0

    def in_race(self) -> bool:
        state = self.reader.get_int("session_state", 0)
        return state in (4, 5)  # racing, checkered

    def private_qualifying(self) -> bool:
        return self.reader.get_int("session_type", 0) in (2, 3)  # qualify

    def in_countdown(self) -> bool:
        state = self.reader.get_int("session_state", 0)
        return state == 3  # countdown

    def in_formation(self) -> bool:
        state = self.reader.get_int("session_state", 0)
        return state == 2  # formation

    def pit_open(self) -> bool:
        flags = self.reader.connector.get_int("SessionFlags", 0)
        return (flags & 0x100) == 0  # pit closed bit; 0 = open

    def pre_race(self) -> bool:
        state = self.reader.get_int("session_state", 0)
        return state in (0, 1, 2, 3)  # invalid, warmup, formation, countdown

    def green_flag(self) -> bool:
        flags = self.reader.connector.get_int("SessionFlags", 0)
        return (flags & 1) != 0  # green

    def blue_flag(self, index: int | None = None) -> bool:
        flags = self.reader.connector.get_int("SessionFlags", 0)
        return (flags & 0x80) != 0  # blue

    def yellow_flag(self) -> bool:
        flags = self.reader.connector.get_int("SessionFlags", 0)
        return (flags & 2) != 0  # yellow

    def start_lights(self) -> int:
        return 0

    def track_temperature(self) -> float:
        return self.reader.get_float("track_surface_temp", 0.0)

    def ambient_temperature(self) -> float:
        return self.reader.get_float("track_air_temp", 0.0)

    def raininess(self) -> float:
        return 0.0

    def wetness_minimum(self) -> float:
        return 0.0

    def wetness_maximum(self) -> float:
        return 0.0

    def wetness_average(self) -> float:
        return 0.0

    def wetness(self) -> tuple[float, float, float]:
        return (0.0, 0.0, 0.0)

    def weather_forecast(self) -> tuple[WeatherNode, ...]:
        return ()

    def time_scale(self) -> int:
        return 1


class Switch(_reader.Switch, _Adapter):
    def headlights(self, index: int | None = None) -> int:
        return self.reader.get_int("headlights", 0)

    def ignition_starter(self, index: int | None = None) -> int:
        return self.reader.get_int("ignition", 0)

    def speed_limiter(self, index: int | None = None) -> int:
        return self.reader.get_int("speed_limiter", 0)

    def drs_status(self, index: int | None = None) -> int:
        return 0

    def auto_clutch(self) -> bool:
        return False


class Timing(_reader.Timing, _Adapter):
    def start(self, index: int | None = None) -> float:
        return 0.0

    def elapsed(self, index: int | None = None) -> float:
        return self.reader.get_float("current_lap_time", 0.0)

    def current_laptime(self, index: int | None = None) -> float:
        return self.reader.get_float("current_lap_time", 0.0)

    def last_laptime(self, index: int | None = None) -> float:
        idx = 0 if index is None else index
        if idx == 0:
            return self.reader.get_float("last_lap_time", 0.0)
        return self.reader.get_float_at("CarIdxLastLapTime", idx, 0.0)

    def best_laptime(self, index: int | None = None) -> float:
        idx = 0 if index is None else index
        if idx == 0:
            return self.reader.get_float("best_lap_time", 0.0)
        return self.reader.get_float_at("CarIdxBestLapTime", idx, 0.0)

    def reference_laptime(self, index: int | None = None):
        return 0.0

    def estimated_laptime(self, index: int | None = None) -> float:
        lap_est = self.reader.get_float("LapEstTime", 0.0)
        if lap_est > 0:
            return lap_est
        return self.reader.get_float("best_lap_time", 0.0)

    def estimated_time_into(self, index: int | None = None) -> float:
        idx = 0 if index is None else index
        lap_est = self.estimated_laptime()
        if lap_est <= 0:
            return 0.0
        dist_pct = self.reader.get_float("lap_dist_pct", 0.0) if idx == 0 else self.reader.get_float_at("CarIdxLapDistPct", idx, 0.0)
        return float(dist_pct) * lap_est

    def current_sector1(self, index: int | None = None) -> float:
        return 0.0

    def current_sector2(self, index: int | None = None) -> float:
        return 0.0

    def last_sector1(self, index: int | None = None) -> float:
        return 0.0

    def last_sector2(self, index: int | None = None) -> float:
        return 0.0

    def best_sector1(self, index: int | None = None) -> float:
        return 0.0

    def best_sector2(self, index: int | None = None) -> float:
        return 0.0

    def behind_leader(self, index: int | None = None) -> float:
        idx = 0 if index is None else index
        return self.reader.get_float_at("CarIdxTime", idx, 0.0)

    def behind_next(self, index: int | None = None) -> float:
        return 0.0


class Tyre(_reader.Tyre, _Adapter):
    _wheels = (0.0, 0.0, 0.0, 0.0)
    _wheels_ico = (0.0,) * 12

    def _tyre_temps(self) -> tuple[float, float, float, float]:
        """FL, FR, RL, RR from iRacing TireTemp (surface; used also for inner/carcass)."""
        return (
            self.reader.get_float("tire_temp_fl", 0.0),
            self.reader.get_float("tire_temp_fr", 0.0),
            self.reader.get_float("tire_temp_rl", 0.0),
            self.reader.get_float("tire_temp_rr", 0.0),
        )

    def compound_front(self, index: int | None = None) -> int:
        return 0

    def compound_rear(self, index: int | None = None) -> int:
        return 0

    def compound(self, index: int | None = None) -> tuple[int, int]:
        return (0, 0)

    def compound_name_front(self, index: int | None = None) -> str:
        return ""

    def compound_name_rear(self, index: int | None = None) -> str:
        return ""

    def compound_name(self, index: int | None = None) -> tuple[str, str]:
        return ("", "")

    def surface_temperature_avg(self, index: int | None = None) -> tuple[float, ...]:
        return self._tyre_temps()

    def surface_temperature_ico(self, index: int | None = None) -> tuple[float, ...]:
        return self._wheels_ico

    def inner_temperature_avg(self, index: int | None = None) -> tuple[float, ...]:
        return self._tyre_temps()

    def inner_temperature_ico(self, index: int | None = None) -> tuple[float, ...]:
        return self._wheels_ico

    def pressure(self, index: int | None = None) -> tuple[float, ...]:
        return self._wheels

    def load(self, index: int | None = None) -> tuple[float, ...]:
        return self._wheels

    def wear(self, index: int | None = None) -> tuple[float, ...]:
        return (
            self.reader.get_float("tire_wear_fl", 0.0),
            self.reader.get_float("tire_wear_fr", 0.0),
            self.reader.get_float("tire_wear_rl", 0.0),
            self.reader.get_float("tire_wear_rr", 0.0),
        )

    def carcass_temperature(self, index: int | None = None) -> tuple[float, ...]:
        return self._tyre_temps()

    def vertical_deflection(self, index: int | None = None) -> tuple[float, ...]:
        return self._wheels


class Vehicle(_reader.Vehicle, _Adapter):
    def is_player(self, index: int = 0) -> bool:
        return index == self.player_index()

    def is_driving(self) -> bool:
        return self.connector.is_active

    def player_index(self) -> int:
        return self.reader.connector.get_int("DriverCarIdx", 0)

    def slot_id(self, index: int | None = None) -> int:
        return 0

    def driver_name(self, index: int | None = None) -> str:
        idx = 0 if index is None else index
        val = self.reader.connector.get_var_at("CarIdxName", idx, None)
        return str(val).strip() if val else ""

    def vehicle_name(self, index: int | None = None) -> str:
        idx = 0 if index is None else index
        val = self.reader.connector.get_var_at("CarScreenName", idx, None) or self.reader.connector.get_var_at("CarPath", idx, None)
        return str(val).strip() if val else ""

    def class_name(self, index: int | None = None) -> str:
        idx = 0 if index is None else index
        val = self.reader.connector.get_var_at("CarIdxCarClassShortName", idx, None)
        return str(val).strip() if val else ""

    def same_class(self, index: int | None = None) -> bool:
        return True

    def total_vehicles(self) -> int:
        n = self.reader.connector.get_int("DriverCount", 0)
        return max(n, 1) if n > 0 else 1

    def place(self, index: int | None = None) -> int:
        idx = 0 if index is None else index
        pos = self.reader.get_int_at("CarIdxPosition", idx, 1)
        return max(1, pos) if pos else 1

    def qualification(self, index: int | None = None) -> int:
        return self.place(index)

    def in_pits(self, index: int | None = None) -> bool:
        idx = 0 if index is None else index
        surface = self.reader.get_int_at("CarIdxTrackSurface", idx, 0)
        return surface in (2, 3)

    def in_garage(self, index: int | None = None) -> bool:
        idx = 0 if index is None else index
        surface = self.reader.get_int_at("CarIdxTrackSurface", idx, 0)
        return surface == 2

    def in_paddock(self, index: int | None = None) -> int:
        idx = 0 if index is None else index
        surface = self.reader.get_int_at("CarIdxTrackSurface", idx, 0)
        if surface == 0:
            return 0  # on track
        if surface == 2:
            return 2  # garage
        return 1  # pit lane

    def number_pitstops(self, index: int | None = None, penalty: int = 0) -> int:
        idx = 0 if index is None else index
        n = self.reader.get_int_at("CarIdxPitStopCount", idx, 0)
        return max(0, n - penalty) if penalty else max(0, n)

    def number_penalties(self, index: int | None = None) -> int:
        return 0

    def pit_request(self, index: int | None = None) -> bool:
        if index is not None and index != 0:
            return False
        return self.reader.connector.get_int("OnPitRoad", 0) != 0

    def pit_stop_time(self) -> float:
        return 0.0

    def absolute_refill(self) -> float:
        return 0.0

    def stint_usage(self, driver_name: str) -> tuple[float, float, float, float, int]:
        return STINT_USAGE_DEFAULT

    def finish_state(self, index: int | None = None) -> int:
        return 0

    def fuel(self, index: int | None = None) -> float:
        return self.reader.get_float("fuel_level", 0.0)

    def tank_capacity(self, index: int | None = None) -> float:
        return self.reader.get_float("fuel_capacity", 0.0)

    def virtual_energy(self, index: int | None = None) -> float:
        return 0.0

    def max_virtual_energy(self, index: int | None = None) -> float:
        return 0.0

    def orientation_yaw_radians(self, index: int | None = None) -> float:
        return 0.0

    def position_xyz(self, index: int | None = None) -> tuple[float, float, float]:
        return (0.0, 0.0, 0.0)

    def position_longitudinal(self, index: int | None = None) -> float:
        return 0.0

    def position_lateral(self, index: int | None = None) -> float:
        return 0.0

    def position_vertical(self, index: int | None = None) -> float:
        return 0.0

    def accel_lateral(self, index: int | None = None) -> float:
        return self.reader.get_float("accel_y", 0.0)

    def accel_longitudinal(self, index: int | None = None) -> float:
        return self.reader.get_float("accel_x", 0.0)

    def accel_vertical(self, index: int | None = None) -> float:
        return self.reader.get_float("accel_z", 0.0)

    def velocity_lateral(self, index: int | None = None) -> float:
        return 0.0

    def velocity_longitudinal(self, index: int | None = None) -> float:
        return 0.0

    def velocity_vertical(self, index: int | None = None) -> float:
        return 0.0

    def speed(self, index: int | None = None) -> float:
        return self.reader.get_float("speed", 0.0)

    def downforce_front(self, index: int | None = None) -> float:
        return 0.0

    def downforce_rear(self, index: int | None = None) -> float:
        return 0.0

    def damage_severity(self, index: int | None = None) -> tuple[int, int, int, int, int, int, int, int]:
        return (0,) * 8

    def aero_damage(self, index: int | None = None) -> float:
        return 0.0

    def integrity(self, index: int | None = None) -> float:
        return 1.0

    def is_detached(self, index: int | None = None) -> bool:
        return False

    def impact_time(self, index: int | None = None) -> float:
        return 0.0

    def impact_magnitude(self, index: int | None = None) -> float:
        return 0.0

    def impact_position(self, index: int | None = None) -> tuple[float, float]:
        return (0.0, 0.0)


class Wheel(_reader.Wheel, _Adapter):
    _wheels = (0.0, 0.0, 0.0, 0.0)
    _bools = (False, False, False, False)

    def camber(self, index: int | None = None) -> tuple[float, ...]:
        return self._wheels

    def toe(self, index: int | None = None) -> tuple[float, ...]:
        return self._wheels

    def toe_symmetric(self, index: int | None = None) -> tuple[float, ...]:
        return self._wheels

    def rotation(self, index: int | None = None) -> tuple[float, ...]:
        return self._wheels

    def velocity_lateral(self, index: int | None = None) -> tuple[float, ...]:
        return self._wheels

    def velocity_longitudinal(self, index: int | None = None) -> tuple[float, ...]:
        return self._wheels

    def slip_angle_fl(self, index: int | None = None) -> float:
        return self.reader.get_float("slip_angle_fl", 0.0)

    def slip_angle_fr(self, index: int | None = None) -> float:
        return self.reader.get_float("slip_angle_fr", 0.0)

    def slip_angle_rl(self, index: int | None = None) -> float:
        return self.reader.get_float("slip_angle_rl", 0.0)

    def slip_angle_rr(self, index: int | None = None) -> float:
        return self.reader.get_float("slip_angle_rr", 0.0)

    def ride_height(self, index: int | None = None) -> tuple[float, ...]:
        return self._wheels

    def third_spring_deflection(self, index: int | None = None) -> tuple[float, ...]:
        return self._wheels

    def suspension_deflection(self, index: int | None = None) -> tuple[float, ...]:
        return (
            self.reader.get_float("suspension_travel_fl", 0.0) * 1000,
            self.reader.get_float("suspension_travel_fr", 0.0) * 1000,
            self.reader.get_float("suspension_travel_rl", 0.0) * 1000,
            self.reader.get_float("suspension_travel_rr", 0.0) * 1000,
        )

    def suspension_force(self, index: int | None = None) -> tuple[float, ...]:
        return self._wheels

    def suspension_damage(self, index: int | None = None) -> tuple[float, ...]:
        return self._wheels

    def position_vertical(self, index: int | None = None) -> tuple[float, ...]:
        return self._wheels

    def is_detached(self, index: int | None = None) -> tuple[bool, ...]:
        return self._bools

    def offroad(self, index: int | None = None) -> int:
        return 0
