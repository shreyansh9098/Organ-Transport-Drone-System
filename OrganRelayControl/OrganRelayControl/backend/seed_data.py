from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from auth import get_password_hash
from datetime import datetime, timedelta
import json

def seed_database():
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        if db.query(models.User).first():
            print("Database already seeded. Skipping...")
            return
        
        print("Seeding database...")
        
        admin_user = models.User(
            username="admin",
            email="admin@dronemed.com",
            hashed_password=get_password_hash("admin123"),
            full_name="System Administrator",
            role=models.UserRole.ADMIN,
            is_active=True
        )
        
        hospital_user = models.User(
            username="hospital1",
            email="hospital@medical.com",
            hashed_password=get_password_hash("hospital123"),
            full_name="Hospital Coordinator",
            role=models.UserRole.HOSPITAL_USER,
            is_active=True
        )
        
        operator_user = models.User(
            username="operator1",
            email="operator@dronemed.com",
            hashed_password=get_password_hash("operator123"),
            full_name="Drone Operator",
            role=models.UserRole.DRONE_OPERATOR,
            is_active=True
        )
        
        emergency_user = models.User(
            username="emergency",
            email="emergency@dronemed.com",
            hashed_password=get_password_hash("emergency123"),
            full_name="Emergency Controller",
            role=models.UserRole.EMERGENCY_CONTROLLER,
            is_active=True
        )
        
        db.add_all([admin_user, hospital_user, operator_user, emergency_user])
        db.commit()
        
        hospitals = [
            models.Hospital(
                name="Central Medical Center",
                address="123 Main St, New York, NY 10001",
                latitude=40.7589,
                longitude=-73.9851,
                contact_phone="+1-555-0101",
                contact_email="central@medical.com",
                is_active=True
            ),
            models.Hospital(
                name="Westside General Hospital",
                address="456 West Ave, New York, NY 10036",
                latitude=40.7614,
                longitude=-73.9776,
                contact_phone="+1-555-0102",
                contact_email="westside@medical.com",
                is_active=True
            ),
            models.Hospital(
                name="East River Medical",
                address="789 East Rd, New York, NY 10002",
                latitude=40.7156,
                longitude=-73.9874,
                contact_phone="+1-555-0103",
                contact_email="eastriver@medical.com",
                is_active=True
            ),
            models.Hospital(
                name="North Point Healthcare",
                address="321 North Blvd, New York, NY 10034",
                latitude=40.8678,
                longitude=-73.9213,
                contact_phone="+1-555-0104",
                contact_email="northpoint@medical.com",
                is_active=True
            ),
        ]
        
        db.add_all(hospitals)
        db.commit()
        
        drones = [
            models.Drone(
                serial_number="DRN-2024-001",
                model="MediFlight Pro X1",
                max_range_km=150.0,
                max_speed_kmh=120.0,
                max_altitude_m=500.0,
                battery_capacity_mah=20000,
                temperature_min=2.0,
                temperature_max=8.0,
                is_active=True,
                current_latitude=40.7589,
                current_longitude=-73.9851,
                current_battery=95.0,
                current_status="idle"
            ),
            models.Drone(
                serial_number="DRN-2024-002",
                model="MediFlight Pro X1",
                max_range_km=150.0,
                max_speed_kmh=120.0,
                max_altitude_m=500.0,
                battery_capacity_mah=20000,
                temperature_min=2.0,
                temperature_max=8.0,
                is_active=True,
                current_latitude=40.7614,
                current_longitude=-73.9776,
                current_battery=88.0,
                current_status="idle"
            ),
            models.Drone(
                serial_number="DRN-2024-003",
                model="CargoMed Heavy Lift",
                max_range_km=200.0,
                max_speed_kmh=100.0,
                max_altitude_m=600.0,
                battery_capacity_mah=30000,
                temperature_min=2.0,
                temperature_max=8.0,
                is_active=True,
                current_latitude=40.7156,
                current_longitude=-73.9874,
                current_battery=100.0,
                current_status="idle"
            ),
        ]
        
        db.add_all(drones)
        db.commit()
        
        now = datetime.utcnow()
        
        route_1 = [[40.7589, -73.9851], [40.7600, -73.9800], [40.7614, -73.9776]]
        mission_1 = models.Mission(
            mission_code="M20240101120000",
            drone_id=1,
            origin_hospital_id=1,
            destination_hospital_id=2,
            operator_id=operator_user.id,
            organ_type="Heart",
            priority_level=5,
            status=models.MissionStatus.COMPLETED,
            planned_route=json.dumps(route_1),
            actual_route=json.dumps(route_1),
            temperature_min=2.0,
            temperature_max=8.0,
            scheduled_start=now - timedelta(hours=2),
            actual_start=now - timedelta(hours=2),
            estimated_arrival=now - timedelta(hours=1, minutes=30),
            actual_arrival=now - timedelta(hours=1, minutes=28),
            distance_km=3.2,
            weather_condition="clear"
        )
        
        route_2 = [[40.7614, -73.9776], [40.7500, -73.9900], [40.7156, -73.9874]]
        mission_2 = models.Mission(
            mission_code="M20240101130000",
            drone_id=2,
            origin_hospital_id=2,
            destination_hospital_id=3,
            operator_id=operator_user.id,
            organ_type="Kidney",
            priority_level=4,
            status=models.MissionStatus.IN_PROGRESS,
            planned_route=json.dumps(route_2),
            temperature_min=2.0,
            temperature_max=8.0,
            scheduled_start=now - timedelta(minutes=30),
            actual_start=now - timedelta(minutes=25),
            estimated_arrival=now + timedelta(minutes=20),
            distance_km=6.5,
            weather_condition="cloudy"
        )
        
        route_3 = [[40.7156, -73.9874], [40.8000, -73.9500], [40.8678, -73.9213]]
        mission_3 = models.Mission(
            mission_code="M20240101140000",
            drone_id=3,
            origin_hospital_id=3,
            destination_hospital_id=4,
            operator_id=operator_user.id,
            organ_type="Liver",
            priority_level=3,
            status=models.MissionStatus.PENDING,
            planned_route=json.dumps(route_3),
            temperature_min=2.0,
            temperature_max=8.0,
            scheduled_start=now + timedelta(hours=1),
            estimated_arrival=now + timedelta(hours=2),
            distance_km=18.5,
            weather_condition="clear"
        )
        
        db.add_all([mission_1, mission_2, mission_3])
        db.commit()
        
        telemetry_points = [
            models.Telemetry(
                mission_id=mission_2.id,
                drone_id=2,
                timestamp=now - timedelta(minutes=20),
                latitude=40.7614,
                longitude=-73.9776,
                altitude_m=150.0,
                speed_kmh=95.0,
                battery_percentage=88.0,
                temperature_celsius=5.2,
                heading=180.0,
                signal_strength=85
            ),
            models.Telemetry(
                mission_id=mission_2.id,
                drone_id=2,
                timestamp=now - timedelta(minutes=15),
                latitude=40.7550,
                longitude=-73.9850,
                altitude_m=165.0,
                speed_kmh=100.0,
                battery_percentage=82.0,
                temperature_celsius=5.5,
                heading=185.0,
                signal_strength=88
            ),
            models.Telemetry(
                mission_id=mission_2.id,
                drone_id=2,
                timestamp=now - timedelta(minutes=10),
                latitude=40.7450,
                longitude=-73.9900,
                altitude_m=170.0,
                speed_kmh=98.0,
                battery_percentage=75.0,
                temperature_celsius=5.8,
                heading=190.0,
                signal_strength=90
            ),
        ]
        
        db.add_all(telemetry_points)
        db.commit()
        
        alert_1 = models.Alert(
            mission_id=mission_1.id,
            alert_type=models.AlertType.TEMPERATURE_DEVIATION,
            severity=models.AlertSeverity.HIGH,
            message="Temperature briefly exceeded maximum threshold",
            value=8.5,
            threshold=8.0,
            is_resolved=True,
            resolved_at=now - timedelta(hours=1, minutes=45),
            resolved_by=operator_user.id
        )
        
        db.add(alert_1)
        db.commit()
        
        settings = [
            models.SystemSettings(
                key="default_temperature_min",
                value="2.0",
                description="Default minimum temperature for organ transport (Celsius)"
            ),
            models.SystemSettings(
                key="default_temperature_max",
                value="8.0",
                description="Default maximum temperature for organ transport (Celsius)"
            ),
            models.SystemSettings(
                key="low_battery_threshold",
                value="20.0",
                description="Battery percentage threshold for low battery alerts"
            ),
        ]
        
        db.add_all(settings)
        db.commit()
        
        print("✓ Created 4 users (admin, hospital1, operator1, emergency)")
        print("✓ Created 4 hospitals")
        print("✓ Created 3 drones")
        print("✓ Created 3 missions (1 completed, 1 in-progress, 1 pending)")
        print("✓ Created sample telemetry data")
        print("✓ Created sample alerts")
        print("✓ Created system settings")
        print("\nDatabase seeded successfully!")
        print("\nDefault login credentials:")
        print("  Admin: admin / admin123")
        print("  Hospital User: hospital1 / hospital123")
        print("  Drone Operator: operator1 / operator123")
        print("  Emergency Controller: emergency / emergency123")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
