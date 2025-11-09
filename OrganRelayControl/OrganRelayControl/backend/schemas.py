from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from models import UserRole, MissionStatus, AlertType, AlertSeverity

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class HospitalBase(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float
    contact_phone: str
    contact_email: str

class HospitalCreate(HospitalBase):
    pass

class Hospital(HospitalBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class DroneBase(BaseModel):
    serial_number: str
    model: str
    max_range_km: float
    max_speed_kmh: float
    max_altitude_m: float
    battery_capacity_mah: int
    temperature_min: float
    temperature_max: float

class DroneCreate(DroneBase):
    pass

class DroneUpdate(BaseModel):
    model: Optional[str] = None
    is_active: Optional[bool] = None
    temperature_min: Optional[float] = None
    temperature_max: Optional[float] = None

class Drone(DroneBase):
    id: int
    is_active: bool
    current_latitude: Optional[float]
    current_longitude: Optional[float]
    current_battery: Optional[float]
    current_status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class MissionBase(BaseModel):
    drone_id: int
    origin_hospital_id: int
    destination_hospital_id: int
    organ_type: str
    priority_level: int
    temperature_min: float
    temperature_max: float
    scheduled_start: datetime

class MissionCreate(MissionBase):
    pass

class Mission(MissionBase):
    id: int
    mission_code: str
    operator_id: int
    status: MissionStatus
    planned_route: Optional[str]
    actual_route: Optional[str]
    actual_start: Optional[datetime]
    estimated_arrival: Optional[datetime]
    actual_arrival: Optional[datetime]
    distance_km: float
    weather_condition: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TelemetryBase(BaseModel):
    latitude: float
    longitude: float
    altitude_m: float
    speed_kmh: float
    battery_percentage: float
    temperature_celsius: float
    heading: Optional[float] = None
    signal_strength: Optional[int] = None

class TelemetryCreate(BaseModel):
    mission_id: int
    drone_id: int
    latitude: float
    longitude: float
    altitude_m: float
    speed_kmh: float
    battery_percentage: float
    temperature_celsius: float
    heading: Optional[float] = None
    signal_strength: Optional[int] = None

class Telemetry(TelemetryCreate):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

class AlertBase(BaseModel):
    mission_id: int
    alert_type: AlertType
    severity: AlertSeverity
    message: str
    value: Optional[float] = None
    threshold: Optional[float] = None

class AlertCreate(AlertBase):
    pass

class Alert(AlertBase):
    id: int
    is_resolved: bool
    resolved_at: Optional[datetime]
    resolved_by: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

class BlockchainEntry(BaseModel):
    id: int
    mission_id: int
    block_index: int
    timestamp: datetime
    data: str
    previous_hash: str
    current_hash: str
    
    class Config:
        from_attributes = True

class RouteOptimizationRequest(BaseModel):
    origin_lat: float
    origin_lon: float
    destination_lat: float
    destination_lon: float
    priority_level: int
    weather_condition: Optional[str] = None

class RouteOptimizationResponse(BaseModel):
    route: List[List[float]]
    distance_km: float
    estimated_time_minutes: float
    weather_score: float
    safety_score: float
    optimized: bool
