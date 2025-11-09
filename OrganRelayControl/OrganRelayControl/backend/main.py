from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict
import json
from datetime import datetime, timedelta
import asyncio

import models
import schemas
import auth
from database import engine, get_db
from blockchain import BlockchainLedger
from ai_optimizer import RouteOptimizer

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Autonomous Organ Transportation Drone System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

@app.get("/")
def read_root():
    return {"message": "Autonomous Organ Transportation Drone System API", "version": "1.0.0"}

@app.post("/api/auth/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(
        (models.User.username == user.username) | (models.User.email == user.email)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/auth/login", response_model=schemas.Token)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()
    
    if not user or not auth.verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token = auth.create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@app.get("/api/auth/me", response_model=schemas.User)
def get_current_user_info(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@app.get("/api/hospitals", response_model=List[schemas.Hospital])
def get_hospitals(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Hospital).filter(models.Hospital.is_active == True).all()

@app.post("/api/hospitals", response_model=schemas.Hospital)
def create_hospital(
    hospital: schemas.HospitalCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role([models.UserRole.ADMIN]))
):
    db_hospital = models.Hospital(**hospital.dict())
    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)
    return db_hospital

@app.get("/api/drones", response_model=List[schemas.Drone])
def get_drones(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Drone).all()

@app.post("/api/drones", response_model=schemas.Drone)
def create_drone(
    drone: schemas.DroneCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role([models.UserRole.ADMIN]))
):
    db_drone = models.Drone(**drone.dict())
    db.add(db_drone)
    db.commit()
    db.refresh(db_drone)
    return db_drone

@app.put("/api/drones/{drone_id}", response_model=schemas.Drone)
def update_drone(
    drone_id: int,
    drone_update: schemas.DroneUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role([models.UserRole.ADMIN, models.UserRole.DRONE_OPERATOR]))
):
    db_drone = db.query(models.Drone).filter(models.Drone.id == drone_id).first()
    if not db_drone:
        raise HTTPException(status_code=404, detail="Drone not found")
    
    for key, value in drone_update.dict(exclude_unset=True).items():
        setattr(db_drone, key, value)
    
    db.commit()
    db.refresh(db_drone)
    return db_drone

@app.get("/api/missions", response_model=List[schemas.Mission])
def get_missions(
    status: str = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    query = db.query(models.Mission)
    if status:
        query = query.filter(models.Mission.status == status)
    return query.order_by(models.Mission.created_at.desc()).all()

@app.get("/api/missions/{mission_id}", response_model=schemas.Mission)
def get_mission(mission_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission

@app.post("/api/missions", response_model=schemas.Mission)
def create_mission(
    mission: schemas.MissionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role([models.UserRole.ADMIN, models.UserRole.HOSPITAL_USER, models.UserRole.EMERGENCY_CONTROLLER]))
):
    origin = db.query(models.Hospital).filter(models.Hospital.id == mission.origin_hospital_id).first()
    destination = db.query(models.Hospital).filter(models.Hospital.id == mission.destination_hospital_id).first()
    
    if not origin or not destination:
        raise HTTPException(status_code=404, detail="Hospital not found")
    
    optimized_route = RouteOptimizer.optimize_route(
        origin.latitude, origin.longitude,
        destination.latitude, destination.longitude,
        mission.priority_level,
        "clear"
    )
    
    mission_code = f"M{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    
    db_mission = models.Mission(
        mission_code=mission_code,
        drone_id=mission.drone_id,
        origin_hospital_id=mission.origin_hospital_id,
        destination_hospital_id=mission.destination_hospital_id,
        operator_id=current_user.id,
        organ_type=mission.organ_type,
        priority_level=mission.priority_level,
        status=models.MissionStatus.PENDING,
        planned_route=json.dumps(optimized_route["route"]),
        temperature_min=mission.temperature_min,
        temperature_max=mission.temperature_max,
        scheduled_start=mission.scheduled_start,
        estimated_arrival=mission.scheduled_start + timedelta(minutes=optimized_route["estimated_time_minutes"]),
        distance_km=optimized_route["distance_km"],
        weather_condition="clear"
    )
    
    db.add(db_mission)
    db.commit()
    db.refresh(db_mission)
    
    return db_mission

@app.put("/api/missions/{mission_id}/start")
def start_mission(
    mission_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role([models.UserRole.DRONE_OPERATOR, models.UserRole.EMERGENCY_CONTROLLER]))
):
    mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    mission.status = models.MissionStatus.IN_PROGRESS
    mission.actual_start = datetime.utcnow()
    
    drone = db.query(models.Drone).filter(models.Drone.id == mission.drone_id).first()
    if drone:
        drone.current_status = "in_flight"
    
    db.commit()
    
    return {"message": "Mission started successfully", "mission_id": mission_id}

@app.post("/api/telemetry", response_model=schemas.Telemetry)
async def ingest_telemetry(
    telemetry: schemas.TelemetryCreate,
    db: Session = Depends(get_db)
):
    db_telemetry = models.Telemetry(**telemetry.dict())
    db.add(db_telemetry)
    
    drone = db.query(models.Drone).filter(models.Drone.id == telemetry.drone_id).first()
    if drone:
        drone.current_latitude = telemetry.latitude
        drone.current_longitude = telemetry.longitude
        drone.current_battery = telemetry.battery_percentage
    
    mission = db.query(models.Mission).filter(models.Mission.id == telemetry.mission_id).first()
    
    alerts = []
    if mission:
        if telemetry.temperature_celsius < mission.temperature_min or telemetry.temperature_celsius > mission.temperature_max:
            alert = models.Alert(
                mission_id=mission.id,
                alert_type=models.AlertType.TEMPERATURE_DEVIATION,
                severity=models.AlertSeverity.CRITICAL,
                message=f"Temperature {telemetry.temperature_celsius}°C outside safe range ({mission.temperature_min}-{mission.temperature_max}°C)",
                value=telemetry.temperature_celsius,
                threshold=mission.temperature_max if telemetry.temperature_celsius > mission.temperature_max else mission.temperature_min
            )
            db.add(alert)
            alerts.append(alert)
        
        if telemetry.battery_percentage < 20:
            severity = models.AlertSeverity.CRITICAL if telemetry.battery_percentage < 10 else models.AlertSeverity.HIGH
            alert = models.Alert(
                mission_id=mission.id,
                alert_type=models.AlertType.LOW_BATTERY,
                severity=severity,
                message=f"Low battery: {telemetry.battery_percentage}%",
                value=telemetry.battery_percentage,
                threshold=20.0
            )
            db.add(alert)
            alerts.append(alert)
    
    db.commit()
    db.refresh(db_telemetry)
    
    telemetry_data = {
        "type": "telemetry",
        "mission_id": telemetry.mission_id,
        "drone_id": telemetry.drone_id,
        "latitude": telemetry.latitude,
        "longitude": telemetry.longitude,
        "altitude_m": telemetry.altitude_m,
        "speed_kmh": telemetry.speed_kmh,
        "battery_percentage": telemetry.battery_percentage,
        "temperature_celsius": telemetry.temperature_celsius,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    BlockchainLedger.add_telemetry_block(db, telemetry.mission_id, telemetry_data)
    
    await manager.broadcast(telemetry_data)
    
    for alert in alerts:
        alert_data = {
            "type": "alert",
            "mission_id": mission.id,
            "alert_type": alert.alert_type.value,
            "severity": alert.severity.value,
            "message": alert.message,
            "timestamp": datetime.utcnow().isoformat()
        }
        await manager.broadcast(alert_data)
        BlockchainLedger.add_alert_block(db, mission.id, alert_data)
    
    return db_telemetry

@app.get("/api/missions/{mission_id}/telemetry", response_model=List[schemas.Telemetry])
def get_mission_telemetry(
    mission_id: int,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return db.query(models.Telemetry).filter(
        models.Telemetry.mission_id == mission_id
    ).order_by(models.Telemetry.timestamp.desc()).limit(limit).all()

@app.get("/api/missions/{mission_id}/alerts", response_model=List[schemas.Alert])
def get_mission_alerts(
    mission_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return db.query(models.Alert).filter(
        models.Alert.mission_id == mission_id
    ).order_by(models.Alert.created_at.desc()).all()

@app.get("/api/alerts", response_model=List[schemas.Alert])
def get_all_alerts(
    resolved: bool = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    query = db.query(models.Alert)
    if resolved is not None:
        query = query.filter(models.Alert.is_resolved == resolved)
    return query.order_by(models.Alert.created_at.desc()).limit(100).all()

@app.post("/api/route/optimize", response_model=schemas.RouteOptimizationResponse)
def optimize_route(
    request: schemas.RouteOptimizationRequest,
    current_user: models.User = Depends(auth.get_current_user)
):
    result = RouteOptimizer.optimize_route(
        request.origin_lat,
        request.origin_lon,
        request.destination_lat,
        request.destination_lon,
        request.priority_level,
        request.weather_condition or "clear"
    )
    return result

@app.get("/api/missions/{mission_id}/blockchain", response_model=List[schemas.BlockchainEntry])
def get_mission_blockchain(
    mission_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return db.query(models.BlockchainLedger).filter(
        models.BlockchainLedger.mission_id == mission_id
    ).order_by(models.BlockchainLedger.block_index).all()

@app.get("/api/missions/{mission_id}/blockchain/verify")
def verify_mission_blockchain(
    mission_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    is_valid = BlockchainLedger.verify_chain(db, mission_id)
    return {"mission_id": mission_id, "blockchain_valid": is_valid}

@app.get("/api/users", response_model=List[schemas.User])
def get_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role([models.UserRole.ADMIN]))
):
    return db.query(models.User).all()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(json.dumps({"message": "Connected to real-time telemetry stream"}))
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
