from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    HOSPITAL_USER = "hospital_user"
    DRONE_OPERATOR = "drone_operator"
    EMERGENCY_CONTROLLER = "emergency_controller"

class MissionStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABORTED = "aborted"
    EMERGENCY = "emergency"

class AlertType(str, enum.Enum):
    TEMPERATURE_DEVIATION = "temperature_deviation"
    LOW_BATTERY = "low_battery"
    ROUTE_DRIFT = "route_drift"
    GEOFENCE_VIOLATION = "geofence_violation"
    EMERGENCY = "emergency"

class AlertSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(SQLEnum(UserRole))
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Hospital(Base):
    __tablename__ = "hospitals"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    contact_phone = Column(String)
    contact_email = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    missions_from = relationship("Mission", foreign_keys="Mission.origin_hospital_id", back_populates="origin_hospital")
    missions_to = relationship("Mission", foreign_keys="Mission.destination_hospital_id", back_populates="destination_hospital")

class Drone(Base):
    __tablename__ = "drones"
    
    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String, unique=True, index=True)
    model = Column(String)
    max_range_km = Column(Float)
    max_speed_kmh = Column(Float)
    max_altitude_m = Column(Float)
    battery_capacity_mah = Column(Integer)
    temperature_min = Column(Float, default=2.0)
    temperature_max = Column(Float, default=8.0)
    is_active = Column(Boolean, default=True)
    current_latitude = Column(Float, nullable=True)
    current_longitude = Column(Float, nullable=True)
    current_battery = Column(Float, nullable=True)
    current_status = Column(String, default="idle")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    missions = relationship("Mission", back_populates="drone")
    telemetry = relationship("Telemetry", back_populates="drone")

class Mission(Base):
    __tablename__ = "missions"
    
    id = Column(Integer, primary_key=True, index=True)
    mission_code = Column(String, unique=True, index=True)
    drone_id = Column(Integer, ForeignKey("drones.id"))
    origin_hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    destination_hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    operator_id = Column(Integer, ForeignKey("users.id"))
    
    organ_type = Column(String)
    priority_level = Column(Integer, default=1)
    status = Column(SQLEnum(MissionStatus), default=MissionStatus.PENDING)
    
    planned_route = Column(Text)
    actual_route = Column(Text, nullable=True)
    
    temperature_min = Column(Float, default=2.0)
    temperature_max = Column(Float, default=8.0)
    
    scheduled_start = Column(DateTime)
    actual_start = Column(DateTime, nullable=True)
    estimated_arrival = Column(DateTime, nullable=True)
    actual_arrival = Column(DateTime, nullable=True)
    
    distance_km = Column(Float)
    weather_condition = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    drone = relationship("Drone", back_populates="missions")
    origin_hospital = relationship("Hospital", foreign_keys=[origin_hospital_id])
    destination_hospital = relationship("Hospital", foreign_keys=[destination_hospital_id])
    operator = relationship("User")
    telemetry = relationship("Telemetry", back_populates="mission")
    alerts = relationship("Alert", back_populates="mission")
    blockchain_entries = relationship("BlockchainLedger", back_populates="mission")

class Telemetry(Base):
    __tablename__ = "telemetry"
    
    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("missions.id"))
    drone_id = Column(Integer, ForeignKey("drones.id"))
    
    timestamp = Column(DateTime, default=datetime.utcnow)
    latitude = Column(Float)
    longitude = Column(Float)
    altitude_m = Column(Float)
    speed_kmh = Column(Float)
    battery_percentage = Column(Float)
    temperature_celsius = Column(Float)
    
    heading = Column(Float, nullable=True)
    signal_strength = Column(Integer, nullable=True)
    
    mission = relationship("Mission", back_populates="telemetry")
    drone = relationship("Drone", back_populates="telemetry")

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("missions.id"))
    
    alert_type = Column(SQLEnum(AlertType))
    severity = Column(SQLEnum(AlertSeverity))
    message = Column(Text)
    value = Column(Float, nullable=True)
    threshold = Column(Float, nullable=True)
    
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime, nullable=True)
    resolved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    mission = relationship("Mission", back_populates="alerts")

class BlockchainLedger(Base):
    __tablename__ = "blockchain_ledger"
    
    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("missions.id"))
    
    block_index = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    data = Column(Text)
    previous_hash = Column(String)
    current_hash = Column(String)
    
    mission = relationship("Mission", back_populates="blockchain_entries")

class SystemSettings(Base):
    __tablename__ = "system_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value = Column(String)
    description = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
